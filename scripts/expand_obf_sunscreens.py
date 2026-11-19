"""Build a local, auditable OBF sunscreen extension using Loredana's V2 helpers."""
import json, re, sys
from pathlib import Path
from urllib.parse import quote_plus
import pandas as pd
import loredana_preparation as prep
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from swan_ui.split_panel.routine_model import ingredient_keys
EU = {'en:'+x for x in ['france','germany','spain','italy','netherlands','belgium','sweden','denmark','poland','portugal','austria','finland','ireland','romania','czech-republic','greece','bulgaria','hungary','croatia','slovakia','slovenia','lithuania','latvia','estonia','luxembourg','malta','cyprus']}
# Human-reviewed identity, primary sunscreen use, facial use and declared SPF.
REVIEWS = {
 '3282770141214': dict(name='Intense Protect SPF 50+', spf='50+', face_body=True, fragrance_free=True, source='https://www.pharmacie-place-ronde.fr/protection-solaire-indice-fort/12304-intense-protect-fluide-solaire-sans-parfum-spf-50-avene.html'),
 '3337875917407': dict(name='Anthelios UVMune 400 anti-dark-spot fluid SPF 50+', spf='50+', face_body=False, fragrance_free=True, source='https://www.aesiel.com/protection-solaire/3914-la-roche-posay-anthelios-50-uvmune-400-fluide-anti-taches-50ml.html'),
 '3337875932349': dict(name='Anthelios UVAIR serum sunscreen SPF 50+', spf='50+', face_body=False, fragrance_free=False, source='https://www.laroche-posay.fr/anthelios/anthelios-uvair-spf50-/3337875932349.html'),
 '3282770145175': dict(name='Keracnyl UV anti-blemish fluid SPF 50+', spf='50+', face_body=False, fragrance_free=False, source='https://www.easypara.com/fluide-anti-imperfections-spf50-50ml-keracnyl-oily-skin-with-a-tendency-to-acne-ducray.html'),
 '3770000717587': dict(name='Lait solaire SPF 50+', spf='50+', face_body=True, fragrance_free=False, source='https://www.parapharmelle.com/fr/parapharmelle/11046-la-rosee-lait-solaire-spf50-3770000717587.html'),
 '3662361003204': dict(name='Sun Secure spray SPF 30', spf='30', face_body=True, fragrance_free=False, source='https://www.aesiel.com/protection-solaire/6942-svr-sun-secure-spf30-spray-200ml.html'),
}

def build():
 data=ROOT/'raw_data'; audit=ROOT/'local_review'
 # Immutable local baseline makes the build repeatable.
 for name in ['catalogue_v2.csv','ingredient_matrix_v2.csv']:
  backup=audit/('baseline_'+name)
  if not backup.exists():backup.write_bytes((data/name).read_bytes())
 cat=pd.read_csv(audit/'baseline_catalogue_v2.csv',dtype='string')
 matrix=pd.read_csv(audit/'baseline_ingredient_matrix_v2.csv',dtype='string')
 cosing=pd.read_csv(data/'Swan_CosIng_reference_2026-10-26.csv',dtype='string')
 prep.inci_names=set(cosing.inci_name.dropna().str.lower())
 known=set(cat.code); existing_names=set(zip(cat.brands.fillna('').str.lower().str.strip(),cat.product_name.fillna('').str.lower().str.strip()))
 snapshots=json.loads((audit/'obf_sunscreens_snapshot.json').read_text())
 additions=[]; decisions=[];ingredients_by_code={}
 for p in snapshots:
  code=str(p['code']);name=p.get('product_name') or p.get('product_name_fr') or p.get('product_name_en') or '';brand=p.get('brands','')
  raw=p.get('ingredients_text') or p.get('ingredients_text_fr') or p.get('ingredients_text_en') or ''
  tags=set(p.get('countries_tags',[]));review=REVIEWS.get(code)
  reasons=[]
  if code in known:reasons.append('Already in catalogue; existing row preserved')
  if not tags & EU:reasons.append('No France/EU market tag')
  if not name and not review:reasons.append('Missing product name')
  if not brand:reasons.append('Missing brand')
  parts=[prep.to_inci(x) for x in prep.split_ingredients(raw)] if raw else []
  parts=[x for x in parts if x];coverage=sum(x in prep.inci_names for x in parts)/len(parts) if parts else 0
  if len(parts)<prep.MIN_INGREDIENTS:reasons.append('Missing or fewer than 5 ingredients')
  if coverage<.5:reasons.append('CosIng coverage below 50%')
  lower=' | '.join(parts);rawlower=raw.lower()
  if not prep.has_word(lower,prep.UV_FILTERS):reasons.append('No recognizable UV filter')
  if any(x in lower for x in ['butylphenyl methylpropional','4-methylbenzylidene camphor']):reasons.append('Legacy ingredient flagged for exclusion/review')
  if not review:reasons.append('Exact variant, facial use and SPF not independently reviewed')
  display=review['name'] if review else name
  if (brand.lower().strip(),display.lower().strip()) in existing_names and code not in known:reasons.append('Same brand/name already present')
  parfum=bool(re.search(r'\b(parfum|fragrance|perfume|aroma|flagrance)\b',rawlower))
  if review and review['fragrance_free'] and parfum:reasons.append('Source fragrance-free claim contradicts OBF ingredient list')
  decision=dict(code=code,product_name=display,brand=brand,france='en:france' in tags,ingredient_count=len(parts),cosing_coverage=round(coverage,3),decision='Hold',reason='; '.join(reasons),obf_url='https://world.openbeautyfacts.org/product/'+code,review_source=review['source'] if review else '')
  if reasons:decisions.append(decision);continue
  row={col:pd.NA for col in cat.columns}
  row.update(role='sunscreen',code=code,product_name=display,brands=brand,brand_display=brand.split(',')[0].strip(),france='en:france' in tags,eu=bool(tags&EU),ingredients_text=raw,inci_text=lower,nb_ingredients=len(parts),coverage=round(coverage,2),inci_to_complete=False,inci_status='complete',in_scope=True,is_recommendable=True,catalogue_review_complete=True,policy_rule='S02' if review['face_body'] else 'S01',policy_decision='Include',final_decision='Include',latest_decision='Include',is_duplicate_v2=False,is_duplicate=False,has_banned_eu=False,rinse_mode='leave-on')
  row['texture']=prep.find_texture(lower,display,'sunscreen');row['is_light']=row['texture']=='light';row['is_rich']=row['texture']=='rich';row['suits_skin']=prep.SKIN_BY_TEXTURE[row['texture']]
  for field,words in {'has_fragrance_allergen':prep.FRAGRANCE_ALLERGENS,'has_acne_active':prep.ACNE_ACTIVES,'has_essential_oil':prep.ESSENTIAL_OILS,'has_retinoid':['retinol','retinal','retinyl','retinoate','retinaldehyde'],'has_strong_acid':['glycolic acid','lactic acid','mandelic acid'],'has_uv_filter':prep.UV_FILTERS,'has_dry_skin_active':['ceramide','urea','butyrospermum parkii butter','squalane','panthenol']}.items():row[field]=prep.has_word(lower,words)
  row['has_parfum']=parfum;row['has_alcohol_denat']='alcohol denat' in lower
  row['is_gentle']=not any(row[f] for f in ['has_parfum','has_essential_oil','has_alcohol_denat','has_retinoid','has_strong_acid'])
  row['has_animal_ingredient']=prep.has_animal(lower);row['animal_uncertain']=prep.is_uncertain(lower);row['is_vegan']=not row['has_animal_ingredient'] and not row['animal_uncertain']
  row['has_pregnancy_avoid']=prep.has_word(lower,['retinol','retinal','retinyl','retinoate','retinaldehyde','tretinoin','adapalene','tazarotene','isotretinoin','hydroquinone']);row['is_pregnancy_ok']=not row['has_pregnancy_avoid'] and not row['has_essential_oil']
  row['is_face_and_body']=review['face_body'];row['is_baby']=False
  for field,word in [('has_salicylic_acid','salicylic acid'),('has_betaine_salicylate','betaine salicylate'),('has_glycerin','glycerin'),('has_petrolatum','petrolatum'),('has_panthenol','panthenol'),('has_ceramides','ceramide')]:row[field]=word in lower
  # Keep copied description/active heuristic, but do not assert a fragrance-free
  # or vegan certification simply from absence of ingredient tokens.
  row['description']=prep.describe(row);row['badges']=' · '.join((['Fragrance-free'] if review['fragrance_free'] else [])+[x.capitalize() for x in prep.actives_found(lower)[:1]])
  row['key_actives']=', '.join(prep.actives_found(lower));row['description_source']='Template and ingredient signals from Loredana V2; OBF source. Texture is a heuristic, not a clinical assessment.'
  row['review_source_file']='Local OBF expansion 2026-11-19';row['review_status']='Reviewed locally, not approved by Loredana';row['review_evidence_notes']=review['source'];row['sun_protection_verified']=True;row['fragrance_free_verified']=review['fragrance_free'];row['declared_spf_reviewed']=review['spf'];row['sunscreen_review_source']=review['source'];row['price_tier']=pd.NA
  row['name_brand']=brand.lower().strip()+' '+display.lower().strip()
  # Only OBF selected FRONT images; never silently use barcode/ingredients photos.
  row['image_url']=p.get('image_front_url') or pd.NA;row['image_small_url']=p.get('image_front_small_url') or pd.NA;row['has_image']=bool(p.get('image_front_url'));row['image_credit']='Photo: Open Beauty Facts contributors, CC BY-SA';row['product_url']=decision['obf_url'];row['search_text']=row['brand_display']+' '+display;row['shopping_url']='https://www.google.com/search?tbm=shop&q='+quote_plus(row['search_text']);row['amazon_url']='https://www.amazon.fr/s?k='+quote_plus(row['search_text']);row['obf_retrieved_on']='2026-11-19'
  additions.append(row);ingredients_by_code[code]=set(parts);known.add(code);existing_names.add((brand.lower().strip(),display.lower().strip()));decision.update(decision='Include locally',reason='S01/S02 identity and SPF reviewed; >=5 ingredients; >=50% CosIng; UV filter detected');decisions.append(decision)
 extra=pd.DataFrame(additions);combined=pd.concat([cat,extra],ignore_index=True)
 # Match the existing wide matrix schema; model uses raw INCI/CosIng for evidence.
 counts={}
 for text in combined.inci_text.fillna(''):
  for ing in set(str(text).split(' | ')):counts[ing]=counts.get(ing,0)+1
 for ing,count in counts.items():
  if count>=5 and ing not in matrix.columns and ing in prep.inci_names:matrix[ing]=0
 extra_matrix=[]
 for row in additions:
  extra_matrix.append({'code':row['code'],**{c:int(c in ingredients_by_code[row['code']]) for c in matrix.columns if c!='code'}})
 combined_matrix=pd.concat([matrix,pd.DataFrame(extra_matrix)],ignore_index=True)
 assert combined.code.is_unique and combined_matrix.code.is_unique
 assert set(combined.code)==set(combined_matrix.code)
 combined.to_csv(data/'catalogue_v2.csv',index=False);combined_matrix.to_csv(data/'ingredient_matrix_v2.csv',index=False)
 pd.DataFrame(decisions).to_csv(audit/'obf_sunscreen_candidate_audit.csv',index=False)
 extra.to_csv(audit/'obf_sunscreen_additions.csv',index=False)
 (audit/'obf_expansion_summary.json').write_text(json.dumps(dict(snapshot_unique=len(snapshots),added=len(additions),catalogue_total=len(combined),sun_rows=int(combined.role.eq('sunscreen').sum()),new_codes=[r['code'] for r in additions]),indent=2))
 print('Added',len(additions),'of',len(snapshots),'unique candidates; catalogue',len(combined))
 for r in additions:print(r['code'],r['brands'],r['product_name'],'coverage',r['coverage'],'gentle',r['is_gentle'])
if __name__=='__main__':build()
