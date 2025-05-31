from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
import re

class StudentHealthDatabase:
    """Comprehensive database of student ailments and treatments"""
    
    AILMENTS_DB = {
        # Respiratory Issues
        "common_cold": {
            "symptoms": ["runny nose", "sneezing", "congestion", "mild cough", "mild fever", "sore throat"],
            "treatments": ["Rest", "Increase fluid intake", "Paracetamol 500mg every 6 hours", "Saline nasal spray", "Throat lozenges"],
            "medications": ["Paracetamol", "Ibuprofen", "Decongestants", "Cough suppressants"],
            "duration": "5-7 days",
            "prevention": ["Wash hands frequently", "Avoid close contact with sick people", "Don't touch face with unwashed hands"]
        },
        
        "flu": {
            "symptoms": ["high fever", "body aches", "fatigue", "headache", "cough", "chills"],
            "treatments": ["Bed rest", "Fluids", "Paracetamol 1000mg every 6 hours", "Antiviral if within 48 hours"],
            "medications": ["Paracetamol", "Ibuprofen", "Oseltamivir (if prescribed)", "Cough medicine"],
            "duration": "7-10 days",
            "prevention": ["Annual flu vaccination", "Good hygiene", "Avoid crowded places during flu season"]
        },
        
        "bronchitis": {
            "symptoms": ["persistent cough", "mucus production", "chest discomfort", "fatigue", "mild fever"],
            "treatments": ["Rest", "Honey and warm water", "Steam inhalation", "Bronchodilators if prescribed"],
            "medications": ["Cough expectorants", "Bronchodilators", "Antibiotics if bacterial"],
            "duration": "2-3 weeks",
            "prevention": ["Avoid smoking", "Good hygiene", "Stay hydrated"]
        },
        
        "asthma_attack": {
            "symptoms": ["wheezing", "shortness of breath", "chest tightness", "coughing"],
            "treatments": ["Use rescue inhaler", "Sit upright", "Stay calm", "Seek medical help if severe"],
            "medications": ["Salbutamol inhaler", "Prednisolone if prescribed"],
            "duration": "Minutes to hours",
            "prevention": ["Avoid triggers", "Use preventive inhalers", "Monitor peak flow"]
        },
        
        # Gastrointestinal Issues
        "gastroenteritis": {
            "symptoms": ["nausea", "vomiting", "diarrhea", "stomach cramps", "fever", "dehydration"],
            "treatments": ["Oral rehydration solution", "BRAT diet", "Rest", "Probiotics"],
            "medications": ["ORS packets", "Loperamide for diarrhea", "Probiotics"],
            "duration": "3-7 days",
            "prevention": ["Good food hygiene", "Wash hands", "Avoid contaminated food/water"]
        },
        
        "food_poisoning": {
            "symptoms": ["sudden nausea", "vomiting", "diarrhea", "stomach pain", "fever"],
            "treatments": ["Clear fluids", "Electrolyte replacement", "Rest", "Gradual food reintroduction"],
            "medications": ["ORS", "Anti-emetics if severe", "Probiotics"],
            "duration": "1-5 days",
            "prevention": ["Proper food storage", "Cook food thoroughly", "Avoid expired food"]
        },
        
        "acid_reflux": {
            "symptoms": ["heartburn", "chest pain", "regurgitation", "difficulty swallowing"],
            "treatments": ["Avoid trigger foods", "Eat smaller meals", "Elevate head while sleeping"],
            "medications": ["Antacids", "H2 blockers", "Proton pump inhibitors"],
            "duration": "Chronic condition",
            "prevention": ["Avoid spicy foods", "Don't lie down after eating", "Maintain healthy weight"]
        },
        
        "constipation": {
            "symptoms": ["infrequent bowel movements", "hard stools", "straining", "abdominal pain"],
            "treatments": ["Increase fiber intake", "More water", "Exercise", "Stool softeners"],
            "medications": ["Fiber supplements", "Stool softeners", "Laxatives if needed"],
            "duration": "Variable",
            "prevention": ["High fiber diet", "Regular exercise", "Adequate water intake"]
        },
        
        "diarrhea": {
            "symptoms": ["frequent loose stools", "abdominal cramps", "dehydration", "urgency"],
            "treatments": ["Fluid replacement", "BRAT diet", "Probiotics", "Rest"],
            "medications": ["ORS", "Loperamide", "Probiotics"],
            "duration": "2-5 days",
            "prevention": ["Good hygiene", "Safe food practices", "Clean water"]
        },
        
        # Mental Health Issues
        "anxiety": {
            "symptoms": ["excessive worry", "restlessness", "fatigue", "difficulty concentrating", "irritability"],
            "treatments": ["Relaxation techniques", "Regular exercise", "Counseling", "Stress management"],
            "medications": ["SSRIs if prescribed", "Benzodiazepines for acute episodes"],
            "duration": "Variable",
            "prevention": ["Regular exercise", "Adequate sleep", "Stress management", "Social support"]
        },
        
        "depression": {
            "symptoms": ["persistent sadness", "loss of interest", "fatigue", "sleep disturbances", "appetite changes"],
            "treatments": ["Counseling", "Regular exercise", "Social support", "Routine maintenance"],
            "medications": ["Antidepressants if prescribed", "Mood stabilizers"],
            "duration": "Variable",
            "prevention": ["Regular exercise", "Social connections", "Stress management", "Professional help"]
        },
        
        "stress": {
            "symptoms": ["tension", "irritability", "headaches", "sleep problems", "muscle tension"],
            "treatments": ["Relaxation techniques", "Time management", "Exercise", "Adequate sleep"],
            "medications": ["Anxiolytics if severe", "Sleep aids if needed"],
            "duration": "Variable",
            "prevention": ["Time management", "Regular breaks", "Exercise", "Healthy lifestyle"]
        },
        
        "panic_attacks": {
            "symptoms": ["rapid heartbeat", "sweating", "trembling", "shortness of breath", "chest pain"],
            "treatments": ["Deep breathing", "Grounding techniques", "Stay in safe place", "Professional help"],
            "medications": ["Benzodiazepines for acute episodes", "Beta-blockers"],
            "duration": "Minutes",
            "prevention": ["Stress management", "Avoid triggers", "Regular therapy", "Medication compliance"]
        },
        
        # Musculoskeletal Issues
        "back_pain": {
            "symptoms": ["lower back pain", "muscle stiffness", "limited mobility", "muscle spasms"],
            "treatments": ["Rest", "Ice/heat therapy", "Gentle stretching", "Pain relievers"],
            "medications": ["Ibuprofen", "Paracetamol", "Muscle relaxants if needed"],
            "duration": "Few days to weeks",
            "prevention": ["Good posture", "Regular exercise", "Proper lifting technique", "Ergonomic setup"]
        },
        
        "neck_pain": {
            "symptoms": ["neck stiffness", "pain", "headaches", "muscle spasms"],
            "treatments": ["Gentle neck exercises", "Heat therapy", "Pain relievers", "Proper pillow"],
            "medications": ["NSAIDs", "Muscle relaxants"],
            "duration": "Few days to weeks",
            "prevention": ["Good posture", "Ergonomic workstation", "Regular breaks", "Proper pillow"]
        },
        
        "muscle_strain": {
            "symptoms": ["muscle pain", "swelling", "limited range of motion", "muscle spasms"],
            "treatments": ["RICE protocol", "Gentle stretching", "Gradual return to activity"],
            "medications": ["NSAIDs", "Topical analgesics"],
            "duration": "Few days to weeks",
            "prevention": ["Proper warm-up", "Gradual exercise progression", "Good conditioning"]
        },
        
        "shin_splints": {
            "symptoms": ["pain along shin bone", "tenderness", "swelling", "pain during exercise"],
            "treatments": ["Rest", "Ice therapy", "Proper footwear", "Gradual return to activity"],
            "medications": ["NSAIDs", "Topical pain relievers"],
            "duration": "2-6 weeks",
            "prevention": ["Proper footwear", "Gradual training increase", "Cross-training"]
        },
        
        # Headaches and Neurological
        "tension_headache": {
            "symptoms": ["band-like pressure", "mild to moderate pain", "neck tension", "fatigue"],
            "treatments": ["Rest", "Stress management", "Regular sleep", "Pain relievers"],
            "medications": ["Paracetamol", "Ibuprofen", "Aspirin"],
            "duration": "30 minutes to 7 days",
            "prevention": ["Stress management", "Regular sleep", "Stay hydrated", "Regular meals"]
        },
        
        "migraine": {
            "symptoms": ["severe headache", "nausea", "light sensitivity", "sound sensitivity", "visual disturbances"],
            "treatments": ["Dark quiet room", "Cold compress", "Rest", "Prescribed medications"],
            "medications": ["Triptans", "NSAIDs", "Anti-emetics"],
            "duration": "4-72 hours",
            "prevention": ["Identify triggers", "Regular sleep", "Stress management", "Preventive medications"]
        },
        
        "cluster_headache": {
            "symptoms": ["severe unilateral pain", "eye watering", "nasal congestion", "restlessness"],
            "treatments": ["Oxygen therapy", "Triptans", "Avoid alcohol", "Regular sleep"],
            "medications": ["Sumatriptan", "Oxygen", "Verapamil for prevention"],
            "duration": "15 minutes to 3 hours",
            "prevention": ["Avoid alcohol", "Regular sleep pattern", "Preventive medications"]
        },
        
        # Skin Conditions
        "acne": {
            "symptoms": ["blackheads", "whiteheads", "pimples", "cysts", "scarring"],
            "treatments": ["Gentle cleansing", "Topical treatments", "Avoid picking", "Oil-free products"],
            "medications": ["Benzoyl peroxide", "Salicylic acid", "Retinoids", "Antibiotics if severe"],
            "duration": "Chronic condition",
            "prevention": ["Gentle skincare", "Avoid over-washing", "Oil-free products", "Don't pick"]
        },
        
        "eczema": {
            "symptoms": ["dry skin", "itching", "redness", "scaling", "cracking"],
            "treatments": ["Moisturize regularly", "Avoid triggers", "Cool compresses", "Gentle skincare"],
            "medications": ["Topical corticosteroids", "Moisturizers", "Antihistamines"],
            "duration": "Chronic condition",
            "prevention": ["Regular moisturizing", "Avoid harsh soaps", "Identify triggers", "Gentle fabrics"]
        },
        
        "allergic_dermatitis": {
            "symptoms": ["rash", "itching", "swelling", "blisters", "redness"],
            "treatments": ["Avoid allergen", "Cool compresses", "Calamine lotion", "Antihistamines"],
            "medications": ["Topical corticosteroids", "Oral antihistamines", "Cool compresses"],
            "duration": "Few days to weeks",
            "prevention": ["Identify and avoid allergens", "Protective clothing", "Gentle products"]
        },
        
        "cold_sores": {
            "symptoms": ["tingling", "small blisters", "pain", "crusting", "burning sensation"],
            "treatments": ["Antiviral cream", "Pain relief", "Avoid triggers", "Keep area clean"],
            "medications": ["Acyclovir cream", "Oral antivirals if severe", "Pain relievers"],
            "duration": "7-10 days",
            "prevention": ["Avoid triggers", "Sun protection", "Stress management", "Don't share items"]
        },
        
        # Eye and Ear Conditions
        "conjunctivitis": {
            "symptoms": ["red eyes", "itching", "discharge", "tearing", "gritty feeling"],
            "treatments": ["Warm compresses", "Eye hygiene", "Artificial tears", "Avoid touching eyes"],
            "medications": ["Antibiotic drops if bacterial", "Antihistamine drops if allergic"],
            "duration": "5-7 days",
            "prevention": ["Good hygiene", "Don't share towels", "Avoid allergens", "Don't touch eyes"]
        },
        
        "dry_eyes": {
            "symptoms": ["burning", "stinging", "scratchy feeling", "sensitivity to light", "blurred vision"],
            "treatments": ["Artificial tears", "Humidifier", "Screen breaks", "Blink exercises"],
            "medications": ["Lubricating eye drops", "Prescription drops if severe"],
            "duration": "Chronic condition",
            "prevention": ["Regular screen breaks", "Proper lighting", "Stay hydrated", "Humidify air"]
        },
        
        "ear_infection": {
            "symptoms": ["ear pain", "hearing difficulty", "discharge", "fever", "pressure feeling"],
            "treatments": ["Pain relief", "Warm compress", "Keep ear dry", "See doctor if severe"],
            "medications": ["Pain relievers", "Antibiotic drops if prescribed", "Oral antibiotics if needed"],
            "duration": "3-7 days",
            "prevention": ["Keep ears dry", "Avoid cotton swabs", "Treat allergies", "Good hygiene"]
        },
        
        # Sleep and Fatigue Issues
        "insomnia": {
            "symptoms": ["difficulty falling asleep", "frequent waking", "early waking", "daytime fatigue"],
            "treatments": ["Sleep hygiene", "Regular schedule", "Relaxation techniques", "Limit caffeine"],
            "medications": ["Melatonin", "Short-term sleep aids if prescribed"],
            "duration": "Variable",
            "prevention": ["Regular sleep schedule", "Good sleep environment", "Limit screen time", "Exercise"]
        },
        
        "chronic_fatigue": {
            "symptoms": ["persistent tiredness", "weakness", "difficulty concentrating", "muscle pain"],
            "treatments": ["Graded exercise", "Energy management", "Stress reduction", "Adequate sleep"],
            "medications": ["Supplements if deficient", "Pain relievers", "Sleep aids if needed"],
            "duration": "Chronic condition",
            "prevention": ["Balanced lifestyle", "Regular exercise", "Stress management", "Good nutrition"]
        },
        
        "sleep_apnea": {
            "symptoms": ["loud snoring", "breathing interruptions", "daytime sleepiness", "morning headaches"],
            "treatments": ["Weight management", "Sleep position changes", "CPAP if prescribed", "Avoid alcohol"],
            "medications": ["Nasal decongestants", "CPAP therapy"],
            "duration": "Chronic condition",
            "prevention": ["Maintain healthy weight", "Sleep on side", "Avoid alcohol", "Regular exercise"]
        },
        
        # Urological Issues
        "urinary_tract_infection": {
            "symptoms": ["burning urination", "frequent urination", "cloudy urine", "pelvic pain", "urgency"],
            "treatments": ["Increase fluid intake", "Cranberry juice", "Urinate frequently", "Antibiotics if prescribed"],
            "medications": ["Antibiotics", "Pain relievers", "Urinary analgesics"],
            "duration": "3-7 days with treatment",
            "prevention": ["Stay hydrated", "Urinate after intercourse", "Wipe front to back", "Avoid irritants"]
        },
        
        "kidney_stones": {
            "symptoms": ["severe flank pain", "blood in urine", "nausea", "vomiting", "frequent urination"],
            "treatments": ["Increase water intake", "Pain management", "Strain urine", "Medical follow-up"],
            "medications": ["Strong pain relievers", "Alpha blockers", "Anti-nausea medication"],
            "duration": "Days to weeks",
            "prevention": ["Stay well hydrated", "Limit sodium", "Moderate protein", "Avoid oxalate-rich foods"]
        },
        
        # Nutritional and Metabolic
        "iron_deficiency_anemia": {
            "symptoms": ["fatigue", "weakness", "pale skin", "shortness of breath", "cold hands"],
            "treatments": ["Iron-rich foods", "Iron supplements", "Vitamin C with iron", "Address underlying cause"],
            "medications": ["Iron supplements", "Vitamin C", "B12 if deficient"],
            "duration": "Weeks to months",
            "prevention": ["Iron-rich diet", "Regular check-ups", "Address blood loss", "Balanced nutrition"]
        },
        
        "vitamin_d_deficiency": {
            "symptoms": ["bone pain", "muscle weakness", "fatigue", "depression", "frequent infections"],
            "treatments": ["Sun exposure", "Vitamin D supplements", "Fortified foods", "Regular monitoring"],
            "medications": ["Vitamin D3 supplements", "High-dose vitamin D if severe"],
            "duration": "Months",
            "prevention": ["Regular sun exposure", "Fortified foods", "Supplements if needed", "Regular testing"]
        },
        
        "dehydration": {
            "symptoms": ["thirst", "dry mouth", "fatigue", "dizziness", "dark urine"],
            "treatments": ["Increase fluid intake", "Electrolyte replacement", "Rest in cool place", "Monitor urine color"],
            "medications": ["Oral rehydration solutions", "Electrolyte supplements"],
            "duration": "Hours to days",
            "prevention": ["Regular water intake", "Monitor urine color", "Increase fluids in heat", "Limit alcohol"]
        },
        
        # Women's Health Issues
        "menstrual_cramps": {
            "symptoms": ["lower abdominal pain", "back pain", "nausea", "headache", "mood changes"],
            "treatments": ["Heat therapy", "Exercise", "Pain relievers", "Relaxation techniques"],
            "medications": ["NSAIDs", "Hormonal contraceptives", "Antispasmodics"],
            "duration": "2-3 days",
            "prevention": ["Regular exercise", "Healthy diet", "Stress management", "Adequate sleep"]
        },
        
        "yeast_infection": {
            "symptoms": ["vaginal itching", "burning", "thick white discharge", "pain during urination"],
            "treatments": ["Antifungal medications", "Probiotics", "Avoid irritants", "Cotton underwear"],
            "medications": ["Antifungal creams", "Oral antifungals", "Probiotics"],
            "duration": "3-7 days with treatment",
            "prevention": ["Good hygiene", "Cotton underwear", "Avoid douching", "Limit antibiotics"]
        },
        
        # Dental Issues
        "tooth_pain": {
            "symptoms": ["throbbing pain", "sensitivity", "swelling", "bad taste", "fever"],
            "treatments": ["Pain relievers", "Salt water rinse", "Cold compress", "See dentist urgently"],
            "medications": ["NSAIDs", "Antibiotics if infection", "Topical analgesics"],
            "duration": "Until treated",
            "prevention": ["Regular brushing", "Flossing", "Regular dental check-ups", "Limit sugar"]
        },
        
        "gum_disease": {
            "symptoms": ["bleeding gums", "swelling", "bad breath", "receding gums", "loose teeth"],
            "treatments": ["Improved oral hygiene", "Professional cleaning", "Antibacterial mouthwash", "Dental treatment"],
            "medications": ["Antibacterial mouthwash", "Antibiotics if severe"],
            "duration": "Chronic condition",
            "prevention": ["Regular brushing", "Flossing", "Regular dental visits", "Quit smoking"]
        },
        
        # Sports and Exercise Related
        "heat_exhaustion": {
            "symptoms": ["heavy sweating", "weakness", "nausea", "headache", "muscle cramps"],
            "treatments": ["Move to cool place", "Remove excess clothing", "Cool water", "Electrolyte replacement"],
            "medications": ["Electrolyte solutions", "Pain relievers for headache"],
            "duration": "Hours",
            "prevention": ["Stay hydrated", "Avoid peak heat", "Gradual acclimatization", "Light clothing"]
        },
        
        "exercise_induced_asthma": {
            "symptoms": ["coughing", "wheezing", "shortness of breath", "chest tightness", "fatigue"],
            "treatments": ["Pre-exercise inhaler", "Proper warm-up", "Avoid cold air", "Gradual cool-down"],
            "medications": ["Bronchodilator inhaler", "Preventive inhalers"],
            "duration": "During and after exercise",
            "prevention": ["Pre-exercise medication", "Proper warm-up", "Avoid triggers", "Good conditioning"]
        }
    }
    
    EMERGENCY_SYMPTOMS = [
        "chest pain", "difficulty breathing", "severe bleeding", "unconscious", "severe allergic reaction",
        "suicidal thoughts", "stroke symptoms", "severe head injury", "poisoning", "severe burns",
        "broken bones", "seizures", "severe abdominal pain", "high fever with rash", "anaphylaxis"
    ]
    
    @classmethod
    def identify_ailment(cls, symptoms, duration=None, severity=None):
        """Identify the most likely ailment based on symptoms"""
        if not symptoms:
            return None
            
        symptom_matches = {}
        symptoms_lower = [s.lower() for s in symptoms]
        
        for ailment, data in cls.AILMENTS_DB.items():
            match_score = 0
            ailment_symptoms = [s.lower() for s in data["symptoms"]]
            
            for symptom in symptoms_lower:
                for ailment_symptom in ailment_symptoms:
                    if symptom in ailment_symptom or ailment_symptom in symptom:
                        match_score += 1
                        break
            
            if match_score > 0:
                symptom_matches[ailment] = {
                    "score": match_score,
                    "total_symptoms": len(ailment_symptoms),
                    "match_percentage": (match_score / len(ailment_symptoms)) * 100,
                    "user_match_percentage": (match_score / len(symptoms_lower)) * 100
                }
        
        if not symptom_matches:
            return None
            
        best_matches = sorted(
            symptom_matches.items(), 
            key=lambda x: (x[1]["score"], x[1]["match_percentage"]), 
            reverse=True
        )
        
        return best_matches[0][0] if best_matches else None
    
    @classmethod
    def check_emergency(cls, symptoms):
        """Check if symptoms indicate emergency situation"""
        if not symptoms:
            return False
            
        symptoms_lower = [s.lower() for s in symptoms]
        for symptom in symptoms_lower:
            for emergency_symptom in cls.EMERGENCY_SYMPTOMS:
                if emergency_symptom in symptom or symptom in emergency_symptom:
                    return True
        return False


class ActionIdentifyAilment(Action):
    """Action to identify ailment based on symptoms"""
    
    def name(self) -> Text:
        return "action_identify_ailment"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        symptoms = tracker.get_slot("symptoms")
        duration = tracker.get_slot("duration")
        severity = tracker.get_slot("severity")
        
        if not symptoms:
            dispatcher.utter_message(text="I need to know your symptoms first. What are you experiencing?")
            return []
        
        if StudentHealthDatabase.check_emergency(symptoms):
            return [SlotSet("emergency_case", True)]
        
        ailment = StudentHealthDatabase.identify_ailment(symptoms, duration, severity)
        
        if ailment:
            ailment_data = StudentHealthDatabase.AILMENTS_DB[ailment]
            display_name = ailment.replace("_", " ").title()
            
            message = f"🩺 **Possible Condition: {display_name}**\n\n"
            message += f"🕒 **Typical Duration:** {ailment_data['duration']}\n\n"
            message += f"📋 **Common Symptoms Include:**\n"
            for symptom in ailment_data['symptoms'][:5]:
                message += f"• {symptom.capitalize()}\n"
            
            if len(ailment_data['symptoms']) > 5:
                message += f"• And {len(ailment_data['symptoms']) - 5} more symptoms\n"
            
            dispatcher.utter_message(text=message)
            return [SlotSet("identified_ailment", ailment)]
        else:
            dispatcher.utter_message(
                text="I couldn't identify a specific condition based on your symptoms. "
                     "This could be due to various factors. I recommend consulting with a "
                     "healthcare professional for proper evaluation."
            )
            return []


class ActionRecommendTreatment(Action):
    """Action to recommend treatment based on identified ailment"""
    
    def name(self) -> Text:
        return "action_recommend_treatment"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ailment = tracker.get_slot("identified_ailment")
        severity = tracker.get_slot("severity")
        
        if not ailment or ailment not in StudentHealthDatabase.AILMENTS_DB:
            dispatcher.utter_message(text="I need to identify your condition first before recommending treatment.")
            return []
        
        ailment_data = StudentHealthDatabase.AILMENTS_DB[ailment]
        
        message = f"💊 **Recommended Treatments:**\n\n"
        message += f"🏠 **Home Care:**\n"
        for i, treatment in enumerate(ailment_data['treatments'], 1):
            message += f"{i}. {treatment}\n"
        
        message += f"\n💊 **Medications (Over-the-counter):**\n"
        for i, medication in enumerate(ailment_data['medications'], 1):
            message += f"{i}. {medication}\n"
        
        if severity == "severe":
            message += f"\n⚠️ **Note:** Since you rated your symptoms as severe, "
            message += f"consider seeking medical attention sooner rather than later.\n"
        elif severity == "mild":
            message += f"\n📝 **Note:** Your symptoms are mild, so home remedies may be sufficient. "
            message += f"Monitor your condition and seek help if symptoms worsen.\n"
        
        message += f"\n⏳ **Expected Recovery Time:** {ailment_data['duration']}\n"
        message += f"\n⚠️ **When to see a doctor:**\n"
        message += f"• Symptoms worsen or don't improve after expected duration\n"
        message += f"• High fever (>101.3°F/38.5°C)\n"
        message += f"• Severe pain or discomfort\n"
        message += f"• Signs of complications\n"
        
        dispatcher.utter_message(text=message)
        dispatcher.utter_message(template="utter_disclaimer")
        
        return []


class ActionCheckEmergency(Action):
    """Action to handle emergency situations"""
    
    def name(self) -> Text:
        return "action_check_emergency"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        symptoms = tracker.get_slot("symptoms") or []
        
        events = tracker.events
        user_messages = []
        for event in events:
            if event.get("event") == "user" and event.get("text"):
                user_messages.append(event.get("text").lower())
        
        emergency_keywords = [
            "can't breathe", "chest pain", "heart attack", "stroke", "bleeding heavily",
            "vomiting blood", "severe pain", "broken", "can't move", "suicidal",
            "emergency", "help me", "dying", "unconscious", "seizure", "poisoned"
        ]
        
        is_emergency = False
        for message in user_messages:
            for keyword in emergency_keywords:
                if keyword in message:
                    is_emergency = True
                    break
        
        if is_emergency or StudentHealthDatabase.check_emergency(symptoms):
            dispatcher.utter_message(template="utter_emergency_alert")
            return [SlotSet("emergency_case", True), AllSlotsReset()]
        
        return [SlotSet("emergency_case", False)]


class ActionProvideMedicationInfo(Action):
    """Action to provide detailed medication information"""
    
    def name(self) -> Text:
        return "action_provide_medication_info"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ailment = tracker.get_slot("identified_ailment")
        
        if not ailment or ailment not in StudentHealthDatabase.AILMENTS_DB:
            dispatcher.utter_message(text="Please tell me your symptoms first so I can recommend appropriate medications.")
            return []
        
        ailment_data = StudentHealthDatabase.AILMENTS_DB[ailment]
        
        medication_info = {
            "paracetamol": {
                "dosage": "500-1000mg every 6 hours (max 4g/day)",
                "notes": "Good for pain and fever. Take with food if stomach sensitive."
            },
            "ibuprofen": {
                "dosage": "400-600mg every 6-8 hours (max 2.4g/day)",
                "notes": "Anti-inflammatory. Take with food. Avoid if stomach ulcers."
            },
            "aspirin": {
                "dosage": "300-600mg every 4 hours (max 4g/day)",
                "notes": "Avoid if under 16. Take with food."
            }
        }
        
        message = f"💊 **Detailed Medication Guide:**\n\n"
        
        for medication in ailment_data['medications']:
            med_lower = medication.lower()
            message += f"💊 **{medication}**\n"
            for med_key, info in medication_info.items():
                if med_key in med_lower:
                    message += f"   • Dosage: {info['dosage']}\n"
                    message += f"   • Notes: {info['notes']}\n"
                    break
            else:
                message += f"   • Follow package instructions or consult pharmacist\n"
            message += "\n"
        
        message += f"⚠️ **Important Safety Information:**\n"
        message += f"• Always read labels and follow dosage instructions\n"
        message += f"• Don't exceed maximum daily doses\n"
        message += f"• Check for drug interactions\n"
        message += f"• Consult pharmacist if unsure\n"
        message += f"• Stop and seek help if adverse reactions occur\n"
        
        dispatcher.utter_message(text=message)
        
        return []


class ActionGivePreventionTips(Action):
    """Action to provide prevention tips"""
    
    def name(self) -> Text:
        return "action_give_prevention_tips"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ailment = tracker.get_slot("identified_ailment")
        
        if ailment and ailment in StudentHealthDatabase.AILMENTS_DB:
            ailment_data = StudentHealthDatabase.AILMENTS_DB[ailment]
            display_name = ailment.replace("_", " ").title()
            
            message = f"🛡️ **Prevention Tips for {display_name}:**\n\n"
            for i, tip in enumerate(ailment_data['prevention'], 1):
                message += f"{i}. {tip}\n"
            
            dispatcher.utter_message(text=message)
        
        dispatcher.utter_message(template="utter_prevention_general")
        
        return []


class ActionRestart(Action):
    """Action to restart the conversation"""
    
    def name(self) -> Text:
        return "action_restart"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="🔄 Starting fresh consultation. How can I help you today?")
        return [AllSlotsReset()]


class ValidateSymptomForm(FormValidationAction):
    """Validates the symptom form"""
    
    def name(self) -> Text:
        return "validate_symptom_form"
    
    def validate_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"symptoms": slot_value}
        else:
            dispatcher.utter_message(text="Could you please describe your symptoms?")
            return {"symptoms": None}
    
    def validate_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if slot_value and isinstance(slot_value, str) and any(word in slot_value.lower() for word in ["hours", "days", "weeks", "ago"]):
            return {"duration": slot_value}
        else:
            dispatcher.utter_message(text="Please specify how long you've had these symptoms (e.g., '2 days' or 'a few hours ago').")
            return {"duration": None}
    
    def validate_severity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        valid_severities = ["mild", "moderate", "severe"]
        
        # Check if the slot value is already valid
        if isinstance(slot_value, str):
            slot_value_lower = slot_value.lower()
            if slot_value_lower in valid_severities:
                return {"severity": slot_value_lower}
        
        # Check the latest user message for a severity value
        latest_message = tracker.latest_message.get("text", "").lower()
        for severity in valid_severities:
            if severity in latest_message:
                return {"severity": severity}
        
        # If the slot isn't filled and no valid severity is found in the latest message,
        # return None to let the form's default utter_ask_severity handle the prompt
        # Only dispatch a custom message if the user has already been asked and provided an invalid response
        if tracker.get_slot("requested_slot") == "severity":
            # Check if the user was just asked for severity (i.e., the last bot message was utter_ask_severity)
            last_bot_message = None
            for event in reversed(tracker.events):
                if event.get("event") == "bot" and event.get("text"):
                    last_bot_message = event.get("text")
                    break
            
            # If the last message was the default severity prompt, the user likely gave an invalid response
            if last_bot_message in [
                "On a scale of mild, moderate, to severe, how would you rate your symptoms?",
                "How severe are your symptoms? Would you describe them as mild, moderate, or severe?"
            ]:
                dispatcher.utter_message(text="Please rate your symptoms as mild, moderate, or severe.")
        
        return {"severity": None}


class ActionDefaultFallback(Action):
    """Default fallback action"""
    
    def name(self) -> Text:
        return "action_default_fallback"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(template="utter_default")
        return []