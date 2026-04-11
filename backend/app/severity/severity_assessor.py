"""
Severity Assessment Module

Assesses disease severity using:
- Probability thresholds
- Rule-based medical logic
- Emergency detection
"""

import numpy as np


class SeverityAssessment:
    """
    Assesses the severity of predicted diseases.
    
    Uses probability scores and rule-based medical logic to classify:
    - Low: Mild conditions, low risk
    - Medium: Moderate conditions, medium risk
    - High: Severe conditions, high risk
    - Emergency: Life-threatening, immediate care needed
    """
    
    # Disease severity mapping
    HIGH_SEVERITY_DISEASES = {
        'heart attack': 0.95,
        'stroke': 0.95,
        'severe pneumonia': 0.90,
        'sepsis': 0.90,
        'acute myocardial infarction': 0.95,
        'pulmonary embolism': 0.90,
        'meningitis': 0.90,
        'acute pancreatitis': 0.85,
    }
    
    MEDIUM_SEVERITY_DISEASES = {
        'hypertension': 0.70,
        'diabetes': 0.70,
        'asthma': 0.65,
        'pneumonia': 0.75,
        'bronchitis': 0.60,
        'gastroenteritis': 0.55,
        'urinary tract infection': 0.50,
    }
    
    # Emergency symptom keywords
    EMERGENCY_SYMPTOMS = {
        'chest pain', 'chest discomfort', 'difficulty breathing',
        'shortness of breath', 'severe headache', 'loss of consciousness',
        'unable to speak', 'facial drooping', 'severe bleeding',
        'severe abdominal pain', 'poisoning'
    }
    
    def __init__(self):
        """Initialize severity assessment engine."""
        self.probability_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
    
    def assess_severity(self, disease, probability, symptoms=None, 
                       age=None, vital_signs=None):
        """
        Assess severity of a predicted disease.
        
        Args:
            disease (str): Predicted disease name
            probability (float): Prediction probability (0-1)
            symptoms (list): List of reported symptoms (optional)
            age (float): Patient age (optional)
            vital_signs (dict): Vital signs dict with bp, hr, temp (optional)
            
        Returns:
            dict: Severity assessment with level and reasoning
        """
        severity_level = self._calculate_base_severity(probability)
        
        # Adjust based on disease type
        disease_lower = disease.lower()
        if disease_lower in self.HIGH_SEVERITY_DISEASES:
            severity_level = self._upgrade_severity(severity_level, 'HIGH')
        elif disease_lower in self.MEDIUM_SEVERITY_DISEASES:
            severity_level = self._upgrade_severity(severity_level, 'MEDIUM')
        
        # Check for emergency symptoms
        has_emergency = self._check_emergency_symptoms(symptoms) if symptoms else False
        if has_emergency:
            severity_level = 'EMERGENCY'
        
        # Adjust for age (elderly patients at higher risk)
        if age and age > 65:
            severity_level = self._upgrade_severity(severity_level, None)
        
        # Check vital signs
        vital_risk = self._assess_vital_signs(vital_signs) if vital_signs else 'NORMAL'
        if vital_risk == 'ABNORMAL':
            severity_level = self._upgrade_severity(severity_level, None)
        
        reasoning = self._generate_severity_reasoning(
            disease, probability, severity_level, has_emergency, vital_risk, age
        )
        
        return {
            'severity_level': severity_level,
            'probability': probability,
            'reasoning': reasoning,
            'urgency': self._get_urgency_level(severity_level),
            'recommendation': self._get_recommendation(severity_level)
        }
    
    def _calculate_base_severity(self, probability):
        """
        Calculate base severity from probability.
        
        Args:
            probability (float): Prediction probability
            
        Returns:
            str: Severity level (LOW, MEDIUM, HIGH)
        """
        if probability < self.probability_thresholds['low']:
            return 'LOW'
        elif probability < self.probability_thresholds['medium']:
            return 'LOW'
        elif probability < self.probability_thresholds['high']:
            return 'MEDIUM'
        else:
            return 'HIGH'
    
    def _upgrade_severity(self, current_level, target_level):
        """
        Upgrade severity level.
        
        Args:
            current_level (str): Current severity level
            target_level (str): Target severity level
            
        Returns:
            str: Upgraded severity level
        """
        levels = ['LOW', 'MEDIUM', 'HIGH', 'EMERGENCY']
        current_idx = levels.index(current_level)
        
        if target_level:
            target_idx = levels.index(target_level)
            return levels[max(current_idx, target_idx)]
        else:
            # Upgrade one level
            return levels[min(current_idx + 1, len(levels) - 1)]
    
    def _check_emergency_symptoms(self, symptoms):
        """
        Check if symptoms indicate emergency.
        
        Args:
            symptoms (list): List of reported symptoms
            
        Returns:
            bool: True if emergency symptoms detected
        """
        if not symptoms:
            return False
        
        symptoms_lower = [s.lower() for s in symptoms]
        for emergency_symptom in self.EMERGENCY_SYMPTOMS:
            for symptom in symptoms_lower:
                if emergency_symptom in symptom or symptom in emergency_symptom:
                    return True
        
        return False
    
    def _assess_vital_signs(self, vital_signs):
        """
        Assess vital signs for abnormalities.
        
        Args:
            vital_signs (dict): Dict with systolic_bp, diastolic_bp, hr, temp
            
        Returns:
            str: 'NORMAL' or 'ABNORMAL'
        """
        abnormal_count = 0
        
        # Blood pressure assessment (optimal: < 120/80)
        if vital_signs.get('systolic_bp', 120) > 180 or vital_signs.get('systolic_bp', 120) < 90:
            abnormal_count += 1
        if vital_signs.get('diastolic_bp', 80) > 120 or vital_signs.get('diastolic_bp', 80) < 60:
            abnormal_count += 1
        
        # Heart rate (normal: 60-100)
        hr = vital_signs.get('heart_rate', 80)
        if hr < 50 or hr > 120:
            abnormal_count += 1
        
        # Temperature (normal: 36.5-37.5°C)
        temp = vital_signs.get('temperature', 37)
        if temp < 35 or temp > 39:
            abnormal_count += 1
        
        return 'ABNORMAL' if abnormal_count >= 2 else 'NORMAL'
    
    def _generate_severity_reasoning(self, disease, probability, severity_level,
                                    has_emergency, vital_risk, age):
        """
        Generate reasoning for severity assessment.
        
        Args:
            disease (str): Disease name
            probability (float): Prediction probability
            severity_level (str): Assessed severity level
            has_emergency (bool): Emergency symptoms present
            vital_risk (str): Vital signs assessment
            age (float): Patient age
            
        Returns:
            str: Reasoning text
        """
        reasons = []
        
        reasons.append(f"Disease: {disease} (confidence: {probability*100:.1f}%)")
        
        if severity_level == 'EMERGENCY':
            reasons.append("Emergency symptoms detected - immediate medical attention required")
        
        if age and age > 65:
            reasons.append(f"Advanced age ({age} years) increases risk")
        
        if vital_risk == 'ABNORMAL':
            reasons.append("Abnormal vital signs detected")
        
        return "; ".join(reasons)
    
    def _get_urgency_level(self, severity_level):
        """
        Get urgency level for recommendation.
        
        Args:
            severity_level (str): Severity level
            
        Returns:
            str: Urgency level (Low, Medium, High, Immediate)
        """
        mapping = {
            'LOW': 'Low',
            'MEDIUM': 'Medium',
            'HIGH': 'High',
            'EMERGENCY': 'Immediate'
        }
        return mapping.get(severity_level, 'Low')
    
    def _get_recommendation(self, severity_level):
        """
        Get medical recommendation based on severity.
        
        Args:
            severity_level (str): Severity level
            
        Returns:
            str: Recommendation text
        """
        recommendations = {
            'LOW': 'Consider home care and monitor symptoms. Schedule routine doctor visit.',
            'MEDIUM': 'Schedule urgent doctor appointment within 1-2 days.',
            'HIGH': 'Seek immediate medical consultation or visit emergency room.',
            'EMERGENCY': 'Call emergency services (911/112) immediately or proceed to nearest hospital.'
        }
        return recommendations.get(severity_level, 'Consult with a healthcare provider.')
