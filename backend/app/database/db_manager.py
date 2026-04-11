"""
Database Module

Handles SQLite database operations for storing:
- User inputs
- Prediction results
- Doctor recommendations
"""

import sqlite3
import json
from datetime import datetime
import os


class DatabaseManager:
    """
    Manages SQLite database for healthcare prediction system.
    
    Stores user data, predictions, and doctor recommendations.
    """
    
    def __init__(self, db_path='backend/data/healthcare_predictions.db'):
        """
        Initialize database manager.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.initialize_database()
    
    def get_connection(self):
        """
        Get database connection.
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        return sqlite3.connect(self.db_path)
    
    def initialize_database(self):
        """Initialize database tables if they don't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER,
                gender TEXT,
                height REAL,
                weight REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symptoms TEXT,
                systolic_bp REAL,
                diastolic_bp REAL,
                blood_sugar REAL,
                predicted_disease TEXT,
                probability REAL,
                severity_level TEXT,
                urgency_level TEXT,
                prediction_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Doctor Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctor_recommendations (
                recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                prediction_id INTEGER,
                specialist_type TEXT,
                rank INTEGER,
                relevance_score REAL,
                recommendation_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prediction_id) REFERENCES predictions(prediction_id)
            )
        ''')
        
        # Explanations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS explanations (
                explanation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                prediction_id INTEGER,
                top_features TEXT,
                shap_values TEXT,
                explanation_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prediction_id) REFERENCES predictions(prediction_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, age, gender, height, weight):
        """
        Add a new user to database.
        
        Args:
            age (int): User age
            gender (str): User gender (M/F)
            height (float): Height in cm
            weight (float): Weight in kg
            
        Returns:
            int: User ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (age, gender, height, weight)
            VALUES (?, ?, ?, ?)
        ''', (age, gender, height, weight))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id
    
    def add_prediction(self, user_id, symptoms, systolic_bp, diastolic_bp,
                      blood_sugar, predicted_disease, probability,
                      severity_level, urgency_level, prediction_json):
        """
        Add a prediction record to database.
        
        Args:
            user_id (int): User ID
            symptoms (str): Symptom text
            systolic_bp (float): Systolic blood pressure
            diastolic_bp (float): Diastolic blood pressure
            blood_sugar (float): Blood sugar level
            predicted_disease (str): Primary predicted disease
            probability (float): Disease probability
            severity_level (str): Severity level
            urgency_level (str): Urgency level
            prediction_json (str): Full prediction JSON
            
        Returns:
            int: Prediction ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions
            (user_id, symptoms, systolic_bp, diastolic_bp, blood_sugar,
             predicted_disease, probability, severity_level, urgency_level, prediction_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, symptoms, systolic_bp, diastolic_bp, blood_sugar,
              predicted_disease, probability, severity_level, urgency_level, prediction_json))
        
        prediction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return prediction_id
    
    def add_doctor_recommendation(self, prediction_id, specialist_type,
                                 rank, relevance_score, recommendation_json):
        """
        Add doctor recommendation to database.
        
        Args:
            prediction_id (int): Prediction ID
            specialist_type (str): Type of specialist
            rank (int): Recommendation rank
            relevance_score (float): Relevance score
            recommendation_json (str): Full recommendation JSON
            
        Returns:
            int: Recommendation ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO doctor_recommendations
            (prediction_id, specialist_type, rank, relevance_score, recommendation_json)
            VALUES (?, ?, ?, ?, ?)
        ''', (prediction_id, specialist_type, rank, relevance_score, recommendation_json))
        
        recommendation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return recommendation_id
    
    def add_explanation(self, prediction_id, top_features, shap_values, explanation_text):
        """
        Add explanation to database.
        
        Args:
            prediction_id (int): Prediction ID
            top_features (str): JSON string of top features
            shap_values (str): JSON string of SHAP values
            explanation_text (str): Human-readable explanation
            
        Returns:
            int: Explanation ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO explanations
            (prediction_id, top_features, shap_values, explanation_text)
            VALUES (?, ?, ?, ?)
        ''', (prediction_id, top_features, shap_values, explanation_text))
        
        explanation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return explanation_id
    
    def get_user_predictions(self, user_id):
        """
        Get all predictions for a user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            list: List of prediction records
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM predictions WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        columns = [description[0] for description in cursor.description]
        results = cursor.fetchall()
        conn.close()
        
        return [dict(zip(columns, row)) for row in results]
    
    def get_prediction_details(self, prediction_id):
        """
        Get detailed information for a prediction.
        
        Args:
            prediction_id (int): Prediction ID
            
        Returns:
            dict: Prediction details with recommendations and explanation
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get prediction
        cursor.execute('SELECT * FROM predictions WHERE prediction_id = ?', (prediction_id,))
        prediction = cursor.fetchone()
        
        if not prediction:
            conn.close()
            return None
        
        pred_dict = dict(zip(
            [description[0] for description in cursor.description],
            prediction
        ))
        
        # Get recommendations
        cursor.execute('''
            SELECT * FROM doctor_recommendations
            WHERE prediction_id = ?
            ORDER BY rank
        ''', (prediction_id,))
        
        rec_columns = [description[0] for description in cursor.description]
        recommendations = [dict(zip(rec_columns, row)) for row in cursor.fetchall()]
        
        # Get explanation
        cursor.execute('''
            SELECT * FROM explanations
            WHERE prediction_id = ?
        ''', (prediction_id,))
        
        explanation = cursor.fetchone()
        exp_dict = None
        if explanation:
            exp_columns = [description[0] for description in cursor.description]
            exp_dict = dict(zip(exp_columns, explanation))
        
        conn.close()
        
        return {
            'prediction': pred_dict,
            'recommendations': recommendations,
            'explanation': exp_dict
        }
    
    def get_statistics(self):
        """
        Get database statistics.
        
        Returns:
            dict: Statistics about predictions and users
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        # Total predictions
        cursor.execute('SELECT COUNT(*) FROM predictions')
        total_predictions = cursor.fetchone()[0]
        
        # Most common diseases
        cursor.execute('''
            SELECT predicted_disease, COUNT(*) as count
            FROM predictions
            GROUP BY predicted_disease
            ORDER BY count DESC
            LIMIT 10
        ''')
        common_diseases = cursor.fetchall()
        
        # Average severity
        cursor.execute('''
            SELECT severity_level, COUNT(*) as count
            FROM predictions
            GROUP BY severity_level
        ''')
        severity_distribution = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_users': total_users,
            'total_predictions': total_predictions,
            'common_diseases': common_diseases,
            'severity_distribution': severity_distribution
        }
    
    def close(self):
        """Close database connection."""
        pass  # Connections are closed individually
