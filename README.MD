# Credit Card Transactions Fraud Detection System

## Project Overview

This project focuses on building a machine learning system for detecting fraudulent credit card transactions. It is a team assignment for the **I2425-AI Engineering**. The goal is to design a system fraud detection that minimizes false positives while accurately identifying fraudulent activities.

The demo video is available in the repository: [demo.mp4](https://github.com/thanhtlx/I2425-AI-Engineering/blob/master/demo.mp4)

---

## Key Features

1. **Build Model**: The entire pipeline consists of data filtering, data cleaning, training (with autogluon), validation
2. **Testing**: Unit test and API test
3. **Automated pipeline**: Automated pipeline from build model to deploy model
4. **Non-ML**: Displaying transaction data on GUI
5. **Monitoring**: Use Sentry to monitor and track errors, as well as sending email alerts
6. **Data export**: Export data from Non-ML to re-train the model

---

## Dataset

The project uses a [kaggle public dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection) containing anonymized credit card transaction records. The dataset covers credit cards of 1000 customers doing transactions with a pool of 800 merchants.

---

## Workflow

> **1. Continuous Integration**
>
> - Lint code
> - Run unit tests

> **2. Continuous Delivery**
>
> - Train model
> - Push model to cloud storage

> **3. Continuous Deployment**
>
> - Build and Push Docker Image
> - Deploy to Google Cloud Run
> - Test API endpoint

---

## Repo Structure

```
I2425-AI-Engineering/
├── data/  # Sample data
├── data_preprocessing/  # Data preprocessing, including cleaning, filtering and feature engineering
│   ├── data_cleaning/
│   ├── data_filtering/
│   └── feature_engineering/
├── model_deploying/  # Model deployment and monitoring
├── model_training/  # Model training and validation
├── non_ml/  # Non-ML related files, including backend and frontend source code, Dockerfiles, and deployment scripts
│   ├── be/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml  # Docker compose file for both FE and BE
│   │   ├── .env.sample
|   |   ├── README.md  # Readme for backend
│   │   └── ... (backend source code files)
│   └── fe/
│       ├── Dockerfile
│       ├── .env.sample
|       ├── README.md  # Readme for frontend
│       └── ... (frontend source code files)
├── pipeline/  # Training pipeline
├── scripts/  # Deploy scripts
├── tests/  # Unit tests
├── .gitignore
├── Dockerfile  # ML Dockerfile
├── README.md
└── ... (other project files)
```

## Tools and Technologies

### Version Control: GitHub

### ML flow

- **Programming Languages**: Python 3.10
- **Libraries**:
  - reqs.txt
- **Frameworks**:
  - **Containerize**: Docker
  - **Storage**: Google Cloud Storage
  - **CI/CD**: GitHub Actions
  - Dagshub
  - Google Cloud Run
  - Autogluon

### Non-ML

[![My Skills](https://skillicons.dev/icons?i=fastapi,vue,mysql,docker,sentry&perline=5)](https://skillicons.dev)

- **Backend**: FastAPI
- **Database**: MySQL 8.0
- **Dependency management**: poetry
- **Frontend**: VueJS
- **Containerize**: Docker and docker-compose
- **Performance Monitoring and Error Tracking**: Sentry

---

## Team Members

- 23025107 - **Vũ Trọng Thanh**
- 24025039 - **Nguyễn Trọng Phi**
- 24025040 - **Phạm Bảo Phúc**
- 24025041 - **Phạm Hồng Phúc**

---

## Deliverables

1. **Code Repository**: Well-documented Python scripts.
2. **Video**: Summary of findings and recommendations.
---

## Demo Video
[![Demo Video](https://github.com/thanhtlx/I2425-AI-Engineering/blob/master/thumbnail.png)](https://github.com/thanhtlx/I2425-AI-Engineering/blob/master/demo.mp4)

---

## Acknowledgments

We extend our gratitude to the I2425-AI Engineering instructors for their guidance throughout this project.

---

## License

This project is developed for academic purposes under the [MIT License](LICENSE).
