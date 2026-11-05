"""Check the sequential journey, durable answers, scope and reset."""
from pathlib import Path
from unittest.mock import patch
import pytest
from streamlit.testing.v1 import AppTest
APP=Path(__file__).resolve().parents[1]/'app.py'

@pytest.fixture(autouse=True)
def api_response():
    response={'status':'ok','results':[{'code':str(i),'product_name':f'Test product {i}','reason':'Ingredient indicator','score':2} for i in range(3)]}
    with patch('swan_ui.client.fetch_recommendations',return_value=response):
        yield

def start():
    a=AppTest.from_file(str(APP)).run()
    a.button(key='begin').click().run()
    assert not a.exception
    return a

def next_step(a):
    a.button(key='next_question').click().run()
    assert not a.exception

def complete(a,adult='Yes',concern='Acne-prone skin',flags=None,level=2):
    a.radio(key='q_adult').set_value(adult);next_step(a)
    if adult=='No': return
    a.radio(key='q_concern').set_value(concern);next_step(a)
    if concern!='Acne-prone skin': return
    a.select_slider(key='q_blemish').set_value(level);next_step(a)
    if level>=4: return
    a.multiselect(key='q_flags').set_value(flags or ['None of these']);next_step(a)
    if flags: return
    a.selectbox(key='q_skin').set_value('Dry');next_step(a)
    a.radio(key='q_reactivity').set_value('No');next_step(a)
    a.multiselect(key='q_avoid').set_value(['Fragrance']);next_step(a)
    a.button(key='submit_profile').click().run()
    assert not a.exception



def test_required_answer_blocks_progress():
    a=start();next_step(a)
    assert a.error
    assert a.session_state['question_step']==0

@pytest.mark.parametrize('adult,concern,flags,level,expected',[
    ('Yes','Acne-prone skin',None,2,'results'),
    ('No','Acne-prone skin',None,2,'outside_scope'),
    ('Yes','Dryness / skin barrier',None,2,'coming_soon'),
    ('Yes','Sensitivity / irritation',None,2,'coming_soon'),
    ('Yes','Acne-prone skin',['I use a skin treatment prescribed by a doctor'],2,'professional_guidance'),
    ('Yes','Acne-prone skin',None,5,'professional_guidance'),
])
def test_routes(adult,concern,flags,level,expected):
    a=start();complete(a,adult,concern,flags,level)
    assert a.session_state['view']==expected
    assert len([h for h in a.subheader if h.value.startswith('Test product')])==(3 if expected=='results' else 0)


def test_back_edit_and_confirmed_reset_preserve_then_clear_answers():
    a=start()
    a.radio(key='q_adult').set_value('Yes');next_step(a)
    a.button(key='previous_question').click().run()
    assert a.radio(key='q_adult').value=='Yes'
    complete(a)
    a.button(key='edit').click().run()
    a.button(key='review_4').click().run()
    assert a.selectbox(key='q_skin').value=='Dry'
    a.selectbox(key='q_skin').set_value('Oily');next_step(a)
    assert a.radio(key='q_reactivity').value=='No'
    next_step(a)
    assert a.multiselect(key='q_avoid').value==['Fragrance']
    next_step(a)
    a.button(key='submit_profile').click().run()
    assert a.session_state['profile'].skin_type=='oily'
    a.button(key='reset').click().run()
    a.button(key='cancel_reset').click().run()
    assert 'profile' in a.session_state
    a.button(key='reset').click().run()
    a.button(key='confirm_reset').click().run()
    assert a.session_state['view']=='welcome'
    assert 'answers' not in a.session_state
    a.button(key='begin').click().run()
    assert a.radio(key='q_adult').value is None


def test_conflicting_scope_flags_block_progress():
    a=start()
    a.radio(key='q_adult').set_value('Yes');next_step(a)
    a.radio(key='q_concern').set_value('Acne-prone skin');next_step(a)
    a.select_slider(key='q_blemish').set_value(2);next_step(a)
    a.multiselect(key='q_flags').set_value(['None of these','I use a skin treatment prescribed by a doctor']);next_step(a)
    assert a.error
    assert a.session_state['question_step']==3


@pytest.mark.parametrize("level", [1, 2])
def test_missing_reactivity_has_its_own_message(level):
    a=start()
    a.radio(key='q_adult').set_value('Yes');next_step(a)
    a.radio(key='q_concern').set_value('Acne-prone skin');next_step(a)
    a.select_slider(key='q_blemish').set_value(level);next_step(a)
    a.multiselect(key='q_flags').set_value(['None of these']);next_step(a)
    next_step(a)
    assert a.radio(key='q_reactivity').options==['Yes','No']
    next_step(a)
    assert any('reactivity' in e.value for e in a.error)
    assert not any('blemish' in e.value for e in a.error)
    a.radio(key='q_reactivity').set_value('No');next_step(a)
    next_step(a)
    a.button(key='submit_profile').click().run()
    assert a.session_state['view']=='results'


def test_no_current_blemishes_exits_without_inventing_a_level():
    a=start()
    a.radio(key='q_adult').set_value('Yes');next_step(a)
    a.radio(key='q_concern').set_value('Acne-prone skin');next_step(a)
    a.select_slider(key='q_blemish').set_value('No current blemishes');next_step(a)
    assert a.session_state['view']=='outside_scope'
    assert a.session_state['profile'].blemish_level is None
    assert any('no current blemishes' in x.value for x in a.markdown)
