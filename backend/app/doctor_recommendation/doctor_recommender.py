"""
Doctor Recommendation Engine

Maps predicted diseases to appropriate medical specialists and ranks them.
"""


class DoctorRecommendationEngine:
    """
    Recommends appropriate medical specialists based on predicted diseases.
    
    Maps diseases to specialists and ranks them by disease probability and severity.
    """
    
    # Disease to Specialist Mapping
    DISEASE_SPECIALIST_MAPPING = {
        # Cardiovascular diseases
        'heart attack': ['Cardiologist', 'Emergency Medicine Specialist'],
        'acute myocardial infarction': ['Cardiologist', 'Emergency Medicine Specialist'],
        'heart disease': ['Cardiologist'],
        'hypertension': ['Cardiologist', 'Internal Medicine'],
        'arrhythmia': ['Cardiologist'],
        'heart failure': ['Cardiologist'],
        'stroke': ['Neurologist', 'Emergency Medicine Specialist'],
        
        # Respiratory diseases
        'pneumonia': ['Pulmonologist', 'Internal Medicine'],
        'severe pneumonia': ['Pulmonologist', 'Emergency Medicine Specialist'],
        'asthma': ['Pulmonologist', 'Internal Medicine'],
        'bronchitis': ['Pulmonologist'],
        'tuberculosis': ['Pulmonologist', 'Infectious Disease Specialist'],
        'chronic obstructive pulmonary disease': ['Pulmonologist'],
        'covid-19': ['Infectious Disease Specialist', 'Pulmonologist'],
        
        # Neurological diseases
        'migraine': ['Neurologist'],
        'epilepsy': ['Neurologist'],
        'parkinson disease': ['Neurologist'],
        'alzheimer disease': ['Neurologist'],
        'meningitis': ['Neurologist', 'Infectious Disease Specialist'],
        
        # Gastrointestinal diseases
        'gastroenteritis': ['Gastroenterologist'],
        'peptic ulcer disease': ['Gastroenterologist'],
        'irritable bowel syndrome': ['Gastroenterologist'],
        'crohn disease': ['Gastroenterologist'],
        'ulcerative colitis': ['Gastroenterologist'],
        'hepatitis': ['Gastroenterologist', 'Infectious Disease Specialist'],
        'pancreatitis': ['Gastroenterologist'],
        'acute pancreatitis': ['Gastroenterologist', 'Emergency Medicine Specialist'],
        
        # Endocrine diseases
        'diabetes': ['Endocrinologist', 'Internal Medicine'],
        'thyroid disease': ['Endocrinologist'],
        'hyperthyroidism': ['Endocrinologist'],
        'hypothyroidism': ['Endocrinologist'],
        
        # Infectious diseases
        'malaria': ['Infectious Disease Specialist'],
        'dengue fever': ['Infectious Disease Specialist'],
        'sepsis': ['Infectious Disease Specialist', 'Emergency Medicine Specialist'],
        'urinary tract infection': ['Urologist', 'Internal Medicine'],
        
        # Musculoskeletal diseases
        'arthritis': ['Rheumatologist'],
        'osteoporosis': ['Rheumatologist', 'Orthopedic Surgeon'],
        'fracture': ['Orthopedic Surgeon'],
        'back pain': ['Orthopedic Surgeon', 'Physiotherapist'],
        
        # Blood and cancer
        'anemia': ['Hematologist', 'Internal Medicine'],
        'leukemia': ['Hematologist', 'Oncologist'],
        'cancer': ['Oncologist'],
        
        # Psychiatric/Mental health
        'depression': ['Psychiatrist', 'Clinical Psychologist'],
        'anxiety': ['Psychiatrist', 'Clinical Psychologist'],
        'schizophrenia': ['Psychiatrist'],
        
        # General/Common conditions
        'common cold': ['General Practitioner', 'Internal Medicine'],
        'influenza': ['General Practitioner', 'Internal Medicine'],
        'cough': ['General Practitioner', 'Pulmonologist'],
        'fever': ['General Practitioner', 'Internal Medicine'],
        'headache': ['Neurologist', 'General Practitioner'],
        'fatigue': ['Internal Medicine'],
        'skin rash': ['Dermatologist'],
    }
    
    # Specialist Information
    SPECIALIST_INFO = {
        'Cardiologist': {
            'specialization': 'Heart and cardiovascular diseases',
            'experience_years': 10,
            'availability': 'High'
        },
        'Pulmonologist': {
            'specialization': 'Lung and respiratory diseases',
            'experience_years': 10,
            'availability': 'High'
        },
        'Neurologist': {
            'specialization': 'Nervous system and brain diseases',
            'experience_years': 12,
            'availability': 'Medium'
        },
        'Gastroenterologist': {
            'specialization': 'Digestive system diseases',
            'experience_years': 10,
            'availability': 'High'
        },
        'Endocrinologist': {
            'specialization': 'Hormonal and metabolic diseases',
            'experience_years': 8,
            'availability': 'Medium'
        },
        'Infectious Disease Specialist': {
            'specialization': 'Infections and communicable diseases',
            'experience_years': 10,
            'availability': 'Medium'
        },
        'Orthopedic Surgeon': {
            'specialization': 'Bone and joint diseases',
            'experience_years': 12,
            'availability': 'Medium'
        },
        'Urologist': {
            'specialization': 'Urinary and reproductive system',
            'experience_years': 10,
            'availability': 'Medium'
        },
        'Hematologist': {
            'specialization': 'Blood disorders',
            'experience_years': 12,
            'availability': 'Low'
        },
        'Oncologist': {
            'specialization': 'Cancer treatment',
            'experience_years': 15,
            'availability': 'Low'
        },
        'Psychiatrist': {
            'specialization': 'Mental health and psychiatric disorders',
            'experience_years': 10,
            'availability': 'High'
        },
        'Dermatologist': {
            'specialization': 'Skin diseases',
            'experience_years': 8,
            'availability': 'High'
        },
        'Rheumatologist': {
            'specialization': 'Autoimmune and inflammatory diseases',
            'experience_years': 12,
            'availability': 'Low'
        },
        'General Practitioner': {
            'specialization': 'General medical care',
            'experience_years': 8,
            'availability': 'Very High'
        },
        'Internal Medicine': {
            'specialization': 'Internal diseases and systemic disorders',
            'experience_years': 10,
            'availability': 'High'
        },
        'Emergency Medicine Specialist': {
            'specialization': 'Emergency and acute care',
            'experience_years': 8,
            'availability': 'Very High'
        },
        'Clinical Psychologist': {
            'specialization': 'Mental health and psychological counseling',
            'experience_years': 8,
            'availability': 'High'
        },
        'Physiotherapist': {
            'specialization': 'Physical rehabilitation and therapy',
            'experience_years': 6,
            'availability': 'High'
        }
    }
    
    def __init__(self):
        """Initialize doctor recommendation engine."""
        pass
    
    def recommend_doctors(self, top_diseases, severity_level, urgency_level):
        """
        Recommend doctors based on top predicted diseases.
        
        Args:
            top_diseases (list): List of tuples (disease_name, probability)
            severity_level (str): Severity level (LOW, MEDIUM, HIGH, EMERGENCY)
            urgency_level (str): Urgency level (Low, Medium, High, Immediate)
            
        Returns:
            list: List of recommended doctors with details
        """
        recommended_specialists = []
        
        # Collect all specialists for top diseases
        specialist_scores = {}
        
        for disease, probability in top_diseases[:3]:  # Consider top 3 diseases
            disease_lower = disease.lower()
            
            # Find matching specialists
            specialists = self._find_specialists_for_disease(disease_lower)
            
            for specialist in specialists:
                if specialist not in specialist_scores:
                    specialist_scores[specialist] = 0
                
                # Score based on disease probability and position
                specialist_scores[specialist] += probability
        
        # Rank specialists
        ranked_specialists = sorted(
            specialist_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Build recommendations
        for rank, (specialist, score) in enumerate(ranked_specialists, 1):
            recommendation = {
                'rank': rank,
                'specialist_type': specialist,
                'relevance_score': float(score),
                'urgency': urgency_level,
                'details': self.SPECIALIST_INFO.get(specialist, {}),
                'reason': self._generate_recommendation_reason(
                    specialist, top_diseases, severity_level
                )
            }
            recommended_specialists.append(recommendation)
        
        return recommended_specialists
    
    def _find_specialists_for_disease(self, disease_lower):
        """
        Find all matching specialists for a disease.
        
        Args:
            disease_lower (str): Disease name in lowercase
            
        Returns:
            list: List of specialist types
        """
        # Exact match
        if disease_lower in self.DISEASE_SPECIALIST_MAPPING:
            return self.DISEASE_SPECIALIST_MAPPING[disease_lower]
        
        # Partial match
        for disease_key, specialists in self.DISEASE_SPECIALIST_MAPPING.items():
            if disease_lower in disease_key or disease_key in disease_lower:
                return specialists
        
        # Default to General Practitioner
        return ['General Practitioner', 'Internal Medicine']
    
    def _generate_recommendation_reason(self, specialist, top_diseases, severity_level):
        """
        Generate reason for specialist recommendation.
        
        Args:
            specialist (str): Specialist type
            top_diseases (list): Top predicted diseases
            severity_level (str): Severity level
            
        Returns:
            str: Reason text
        """
        primary_disease = top_diseases[0][0] if top_diseases else "Unknown"
        
        reason = f"Recommended based on predicted condition: {primary_disease}. "
        
        if severity_level == 'EMERGENCY':
            reason += f"{specialist} can provide urgent specialized care for this condition."
        elif severity_level == 'HIGH':
            reason += f"{specialist} specializes in treating this serious condition."
        else:
            reason += f"{specialist} can diagnose and manage this condition effectively."
        
        return reason
    
    def get_specialist_details(self, specialist_type):
        """
        Get detailed information about a specialist.
        
        Args:
            specialist_type (str): Type of specialist
            
        Returns:
            dict: Specialist information
        """
        return self.SPECIALIST_INFO.get(
            specialist_type,
            {'specialization': 'Unknown', 'experience_years': 0, 'availability': 'Unknown'}
        )
