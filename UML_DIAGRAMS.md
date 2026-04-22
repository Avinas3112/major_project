# System UML & Architecture Diagrams

This document contains standard UML and system diagrams for the **Context-Aware Multimodal Disease Prediction System**. These diagrams are written in Mermaid.js and can be viewed directly in VS Code by right-clicking this file and selecting **"Open Preview"**.

---

## 1. Use Case Diagram
Shows the primary interactions between the actors (Patient/User) and the system's core capabilities.

```mermaid
flowchart LR
    %% Actors
    Patient([Patient / User])
    SystemBoundary[Disease Prediction System Modules]
    
    %% Use Cases
    UC1(Enter Symptoms & Demographics)
    UC2(Enter Vital Signs)
    UC3(Predict Disease)
    UC4(View Explainability/SHAP)
    UC5(Get Doctor Recommendations)
    UC6(View Prediction History)
    
    %% Relationships
    Patient --> UC1
    Patient --> UC2
    Patient --> UC6
    
    UC1 --> SystemBoundary
    UC2 --> SystemBoundary
    
    subgraph System Boundary
        SystemBoundary --> UC3
        UC3 --> UC4
        UC3 --> UC5
    end
```

---

## 2. Activity Diagram
Visualizes the step-by-step workflow from the moment a user submits data to system completion.

```mermaid
stateDiagram-v2
    [*] --> FormInput
    FormInput --> Preprocessing
    
    state Preprocessing {
        [*] --> TokenizeText
        TokenizeText --> Lemmatize
        Lemmatize --> ExtractNumericalVitals
        ExtractNumericalVitals --> [*]
    }
    
    Preprocessing --> FeatureExtraction
    FeatureExtraction --> MultimodalFusion
    
    MultimodalFusion --> PredictDisease
    
    PredictDisease --> ParallelExecution
    
    state ParallelExecution {
        [*] --> AssessSeverity
        [*] --> GenerateSHAPExplanation
        [*] --> RecommendDoctor
    }
    
    ParallelExecution --> SaveToDatabase
    SaveToDatabase --> ReturnJSONResponse
    ReturnJSONResponse --> RenderUI
    RenderUI --> [*]
```

---

## 3. Sequence Diagram
Demonstrates the chronological order of messages exchanged between system components for a prediction request.

```mermaid
sequenceDiagram
    actor User
    participant UI as Web Frontend (UI)
    participant API as Flask API
    participant ML as ML Pipeline (Preprocess/Fusion)
    participant Model as Trained Models (LR/RF)
    participant Explainer as SHAP Explainer
    participant DB as SQLite Database

    User->>UI: Fills form & clicks "Predict"
    UI->>API: POST /predict_disease (JSON payload)
    
    API->>ML: Pass symptoms & context
    ML->>ML: NLP Preprocessing & Scaling
    ML->>ML: Multimodal Feature Fusion
    ML-->>API: Transformed Feature Vector
    
    API->>Model: predict_proba(Feature Vector)
    Model-->>API: Top-K Diseases & Confidences
    
    par Parallel Sub-tasks
        API->>Explainer: generate_explanation(models, features)
        Explainer-->>API: SHAP values & reasoning
    and
        API->>API: Assess Severity Level
    and
        API->>API: Map Disease to Doctor Specialist
    end
    
    API->>DB: save_prediction(results)
    DB-->>API: confirmation
    
    API-->>UI: Return JSON {predictions, severity, doctors, explanation}
    UI-->>User: Display Results Dashboard
```

---

## 4. Data Flow Diagram (DFD Level 1)
Shows the flow of data through the system processes and data stores.

```mermaid
flowchart TD
    %% Entities
    U([Patient])
    
    %% Data Stores
    D1[(Models DB: .pkl files)]
    D2[(SQLite Database)]
    
    %% Processes
    P1((1.0 Data<br>Preprocessing))
    P2((2.0 Feature<br>Extraction & Fusion))
    P3((3.0 ML<br>Prediction))
    P4((4.0 Context<br>Assessments))
    
    %% Flows
    U -- "Symptoms, Age, BMI, Vitals" --> P1
    P1 -- "Cleaned Text & Floats" --> P2
    D1 -- "TF-IDF Vocab & Scalers" --> P2
    
    P2 -- "Standardized Vector" --> P3
    D1 -- "Trained Weights (LR/RF)" --> P3
    
    P3 -- "Disease Probabilities" --> P4
    P4 -- "Severity, Explainability, Specialist" --> D2
    U -- "User Demographics" --> D2
    
    P4 -- "Combined Final Diagnosis Report" --> U
```

---

## 5. Collaboration (Communication) Diagram
Visualizes the structural organization and message sequence between objects/modules.

```mermaid
flowchart TD
    UI[Web Application / UI]
    MainAPI[main.py / Flask API Controller]
    
    PP[data_preprocessor.py]
    FE[feature_extractor.py]
    FM[fusion_module.py]
    DP[disease_predictor.py]
    DR[doctor_recommender.py]
    EX[explainer.py]
    DB[db_manager.py]
    
    UI -- "1: User Request Data" --> MainAPI
    MainAPI -- "2: Preprocess text/numbers" --> PP
    MainAPI -- "3: Extract TF-IDF" --> FE
    MainAPI -- "4: Concatenate features" --> FM
    MainAPI -- "5: Predict probabilities" --> DP
    MainAPI -- "6: Explain logic (SHAP)" --> EX
    MainAPI -- "7: Recommend specialists" --> DR
    MainAPI -- "8: Save transaction" --> DB
    MainAPI -- "9: Return JSON payload" --> UI
```