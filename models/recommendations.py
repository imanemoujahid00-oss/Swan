from numbers import Integral

from models.baseline import rank_moisturizers


def filter_avoid(data, avoid):
    selected = data.copy()
    
    if 'fragrance' in avoid:
        selected = selected[
            selected['has_parfum'] == False
        ]
        
    if 'essential_oils' in avoid:
        selected = selected[
            selected['has_essential_oil'] == False
        ]
        
    return selected


def check_scope(profile):
    if type(profile.get('is_adult')) is not bool:
        return 'incomplete_profile'
    
    if profile['is_adult'] == False:
        return 'referral'
    
    if profile.get('concern') not in ['acne_prone', 'other']:
        return 'incomplete_profile'
    
    if profile['concern'] == 'other':
        return 'out_of_scope'
    
    level = profile.get('blemish_level')
    
    if isinstance(level, bool) or not isinstance(level, Integral) or level not in [1, 2, 3, 4, 5]:
        return 'incomplete_profile'
    
    if level >= 4:
        return 'referral'
    
    flags = profile.get('referral_flags')
    
    if not isinstance(flags, list):
        return 'incomplete_profile'
    
    valid_flags = [
        'prescribed_treatment',
        'unusual_lesion',
        'pregnant_or_breastfeeding'
    ]
    
    for flag in flags:
        if flag not in valid_flags:
            return 'incomplete_profile'
        
    if flags:
        return 'referral'
    
    return 'eligible'


def outcome_message(profile, status):
    if status == "incomplete_profile":
        return "Please complete the questionnaire with valid answers."

    if status == "out_of_scope":
        return "Swan only covers acne-prone skin for now."

    if profile["is_adult"] == False:
        return (
            "Swan is made for adults. "
            "Please ask a specialized doctor if needed."
        )

    if profile["blemish_level"] >= 4:
        return (
            "Lots of red, painful or deep spots, or scars, "
            "are worth showing to a doctor or dermatologist."
        )

    referral_messages = {
        "prescribed_treatment": (
            "Check with the person who prescribed your treatment "
            "before adding new products."
        ),
        "unusual_lesion": (
            "A sudden or unusual change in your skin "
            "should be checked by a doctor."
        ),
        "pregnant_or_breastfeeding": (
            "This MVP does not suggest products during pregnancy "
            "or breastfeeding. Please ask a pharmacist or your "
            "healthcare professional for advice."
        )
    }

    messages = []

    for flag, message in referral_messages.items():
        if flag in profile["referral_flags"]:
            messages.append(message)

    return " ".join(messages)



def recommend(profile, data, *, ranker=None):
    status = check_scope(profile)
    
    if status != 'eligible':
        return {
            'status': status,
            'message': outcome_message(profile, status),
            'results': []
        }
    
    valid_skin_types = [
        'oily', 'combination', 'normal', 'dry', 'not_sure'    
    ]
    
    if profile.get('skin_type') not in valid_skin_types:
        return {
            'status': 'incomplete_profile',
            "message": "Please complete the questionnaire with valid answers.",
            'results': []
        }
        
    if type(profile.get('reactivity')) is not bool:
        return {
            'status': 'incomplete_profile',
            "message": "Please complete the questionnaire with valid answers.",
            'results': []
        }
    
    avoid = profile.get('avoid', [])
    
    if not isinstance(avoid, list):
        return {
            'status': 'incomplete_profile',
            "message": "Please complete the questionnaire with valid answers.",
            'results': []
        }
    
    for preference in avoid:
        if preference not in ['fragrance', 'essential_oils']:
            return {
                'status': 'incomplete_profile',
                "message": "Please complete the questionnaire with valid answers.",
                'results': []
            }
            
    selected = filter_avoid(data, avoid)
    
    return (ranker or rank_moisturizers)(selected)
