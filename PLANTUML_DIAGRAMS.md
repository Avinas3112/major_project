# PlantUML Diagrams

Here is the PlantUML code for all the requested software architecture diagrams. If you have the **PlantUML extension** installed in VS Code, you can press `Alt+D` (or `Option+D` on Mac) to preview these directly, or you can paste the blocks into [PlantUML Web Server](http://www.plantuml.com/plantuml).

---

## 1. Use Case Diagram

```plantuml
@startuml
left to right direction
actor "Patient / User" as Patient

package "Disease Prediction System Boundaries" {
    usecase "Enter Symptoms & Demographics" as UC1
    usecase "Enter Vital Signs" as UC2
    usecase "Predict Disease" as UC3
    usecase "View Explainability/SHAP" as UC4
    usecase "Get Doctor Recommendations" as UC5
    usecase "View Prediction History" as UC6
}

Patient --> UC1
Patient --> UC2
Patient --> UC6

UC1 --> UC3
UC2 --> UC3
UC3 --> UC4
UC3 --> UC5
@enduml
```

---

## 2. Activity Diagram

```plantuml
@startuml
start
:Form Input;
partition "Preprocessing" {
    :Tokenize Text;
    :Lemmatize;
    :Extract Numerical Vitals;
}
:Feature Extraction;
:Multimodal Fusion;
:Predict Disease;

fork
    :Assess Severity;
fork again
    :Generate SHAP Explanation;
fork again
    :Recommend Doctor;
end fork

:Save To Database;
:Return JSON Response;
:Render UI;
stop
@enduml
```

---

## 3. Sequence Diagram

```plantuml
@startuml
actor User
participant "Web Frontend (UI)" as UI
participant "Flask API" as API
participant "ML Pipeline\n(Preprocess/Fusion)" as ML
participant "Trained Models\n(LR/RF)" as Model
participant "SHAP Explainer" as Explainer
participant "SQLite Database" as DB

User -> UI: Fills form & clicks "Predict"
UI -> API: POST /predict_disease (JSON payload)

API -> ML: Pass symptoms & context
activate ML
ML -> ML: NLP Preprocessing & Scaling
ML -> ML: Multimodal Feature Fusion
ML -->> API: Transformed Feature Vector
deactivate ML

API -> Model: predict_proba(Feature Vector)
activate Model
Model -->> API: Top-K Diseases & Confidences
deactivate Model

par Parallel Sub-tasks
    API -> Explainer: generate_explanation()
    activate Explainer
    Explainer -->> API: SHAP values & reasoning
    deactivate Explainer
else
    API -> API: Assess Severity Level
else
    API -> API: Map Disease to Doctor Specialist
end

API -> DB: save_prediction(results)
activate DB
DB -->> API: confirmation
deactivate DB

API -->> UI: Return JSON {predictions, severity, doctors, expl.}
UI -->> User: Display Results Dashboard
@enduml
```

---

## 4. Data Flow Diagram (DFD Level 1)
*(PlantUML uses component styling to emulate DFD entity flows)*

```plantuml
@startuml
skinparam componentStyle rectangle

actor "Patient" as U
database "Models DB:\n.pkl files" as D1
database "SQLite Database" as D2

component "1.0 Data\nPreprocessing" as P1
component "2.0 Feature\nExtraction & Fusion" as P2
component "3.0 ML\nPrediction" as P3
component "4.0 Context\nAssessments" as P4

U --> P1 : Symptoms, Age, BMI, Vitals
P1 --> P2 : Cleaned Text & Floats
D1 --> P2 : TF-IDF Vocab & Scalers

P2 --> P3 : Standardized Vector
D1 --> P3 : Trained Weights (LR/RF)

P3 --> P4 : Disease Probabilities
P4 --> D2 : Severity, Explainability, Specialist
U --> D2 : User Demographics

P4 --> U : Combined Final Diagnosis Report
@enduml
```

---

## 5. Collaboration (Communication) Diagram
*(Visualizes the interaction and message ordering between the individual python modules)*

```plantuml
@startuml
object "Web Application / UI" as UI
object "main.py / Flask API" as MainAPI
object "data_preprocessor.py" as PP
object "feature_extractor.py" as FE
object "fusion_module.py" as FM
object "disease_predictor.py" as DP
object "doctor_recommender.py" as DR
object "explainer.py" as EX
object "db_manager.py" as DB

UI -> MainAPI : 1: User Request Data
MainAPI -> PP : 2: Preprocess text/numbers
MainAPI -> FE : 3: Extract TF-IDF
MainAPI -> FM : 4: Concatenate features
MainAPI -> DP : 5: Predict probabilities
MainAPI -> EX : 6: Explain logic (SHAP)
MainAPI -> DR : 7: Recommend specialists
MainAPI -> DB : 8: Save transaction
MainAPI -> UI : 9: Return JSON payload
@enduml
```