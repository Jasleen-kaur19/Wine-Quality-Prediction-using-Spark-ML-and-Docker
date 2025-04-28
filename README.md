# Wine-Quality-Prediction-using-Spark-ML-and-Docker



This project presents a distributed machine learning system designed to predict wine quality using Apache Spark MLlib, deployed across multiple AWS EC2 instances. It encompasses both training and prediction workflows, all containerized with Docker for seamless and scalable deployment.

The primary goal of this assignment is to master the development of parallelized machine learning (ML) applications on the Amazon AWS cloud platform. Throughout this project, you will learn to:

Build and train ML models in parallel using Apache Spark on multiple EC2 instances.

Leverage Spark MLlib for model training, validation, and evaluation in a cloud environment.

Containerize ML applications using Docker to streamline model deployment across different infrastructures.



---

## 📦 Dockerhub Repository

**Dockerhub Repo**: [jasleen4499/wine-predictor](https://hub.docker.com/r/jasleen4499/wine-predictor)


You can pull the Docker image using:
```bash
docker pull jasleen4499/wine-predictor:latest
```

##  🚀 Project Architecture

Step	Details
1)	Launch 4 EC2 instances (1 Master + 3 Workers)
2)	Install and Configure Java, Hadoop, and Spark
3)	SSH Key setup for password-less communication
4)	Start Spark Master and Worker nodes
5)	Train the model on Spark cluster
6)	Build Docker image for prediction
7)	Push Docker image to Dockerhub
8)	Run the model prediction inside Docker container

## Step Implementation:

☁️ Launch EC2 Instances
Instance Type: t2.large

Total Instances: 4 (1 Master + 3 Workers)

VPC: All instances should be in the same VPC and subnet.

Screenshot: ![Screenshot 2025-04-24 at 2 51 03 PM](https://github.com/user-attachments/assets/30e60a6a-8476-437c-8fd8-9779571f5e70)

🛠️ Environment Setup
SSH into Each Instance
```bash
ssh -i "your-key.pem" ec2-user@<instance-public-ip>
```
Setup Passwordless SSH
On all nodes:

```bash
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```
Install Java (OpenJDK 17)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install openjdk-17-jdk wget unzip -y
java -version
```
Add to ~/.bashrc:
```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
export PATH=$JAVA_HOME/bin:$PATH
```
Reload:
```bash
source ~/.bashrc
```
Install Hadoop
```bash
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xvzf hadoop-3.3.6.tar.gz
sudo mv hadoop-3.3.6 /usr/local/hadoop
```
Add to ~/.bashrc:
```bash
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
```
Reload:
```bash
source ~/.bashrc
```
⚙️ Configure Spark
On Master:
```bash
cp $SPARK_HOME/conf/spark-env.sh.template $SPARK_HOME/conf/spark-env.sh
nano $SPARK_HOME/conf/spark-env.sh
```
Add:
```bash
export SPARK_MASTER_HOST=<Master-Private-IP>
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
export HADOOP_HOME=/usr/local/hadoop
```
Edit conf/slaves file:
```bash
<Worker-1-Private-IP>
<Worker-2-Private-IP>
<Worker-3-Private-IP>
```
🔥 Start Spark Cluster
Master:
```bash
$SPARK_HOME/sbin/start-master.sh
$SPARK_HOME/sbin/start-slaves.sh
```
Workers:
```bash
start-slave.sh spark://<Master-Private-IP>:7077
```
SPARK Setup Screenshot:
![Screenshot 2025-04-23 at 10 56 44 AM](https://github.com/user-attachments/assets/ecbea09d-5b02-4cba-ad5b-859941136616)
![Screenshot 2025-04-23 at 10 56 10 AM](https://github.com/user-attachments/assets/31609d19-1c95-42bd-832b-a3b677cbe558)
<img width="1068" alt="Screenshot 2025-04-23 at 10 56 34 AM" src="https://github.com/user-attachments/assets/58aa2b45-15d7-4c46-ad37-9eac5996e013" />
![Screenshot 2025-04-23 at 10 56 21 AM](https://github.com/user-attachments/assets/eba9cbe2-27b6-479d-970c-ce68234cbbea)



Cluster Running Screenshot:
![Screenshot 2025-04-23 at 11 51 19 AM](https://github.com/user-attachments/assets/fe6bd633-c5c9-4e45-96e5-a3aa64fb81d5)

📂 Upload Dataset
Upload datasets to all nodes:
```bash
scp -i "your-key.pem" TrainingDataset.csv ec2-user@<instance-public-ip>:~/
scp -i "your-key.pem" ValidationDataset.csv ec2-user@<instance-public-ip>:~/
```
🧠 Train the Model (Execution on Spark Cluster)
Submit Spark job:
```bash
spark-submit --master spark://<Master-Private-IP>:7077 wine-train.py
```
Training Result:

F1 Score: 0.578

Accuracy: 0.601

Screenshot: ![Screenshot 2025-04-23 at 12 42 02 PM](https://github.com/user-attachments/assets/30c8e575-7f0d-4976-9ebd-1ba04e92fe31)


🧠 Testing the Model
Submit Spark job:
```bash
spark-submit --master spark://<Master-Private-IP>:7077 wine_test.py
```
Testing Result:

F1 Score: 0.561

Accuracy: 0.575

Screenshot: ![Screenshot 2025-04-23 at 1 26 44 PM](https://github.com/user-attachments/assets/217b7b32-80ca-496b-9a8f-ee7c569186cf)

🐳 Build Docker Image
Build the Docker image:
```bash
docker build -t wine-predictor .
```
Screenshot:![Screenshot 2025-04-23 at 2 17 43 PM](https://github.com/user-attachments/assets/419fec2b-10d1-4a11-a1b1-7d6daf641186)


Run the Docker container(Execution on Docker):
```bash
docker run wine-predictor
```

Prediction Output: ![Screenshot 2025-04-23 at 2 18 01 PM](https://github.com/user-attachments/assets/05fe4e65-955c-4dcf-a80f-1341700d4c3c)

Push Docker image to Dockerhub:
```bash
docker push jasleen4499/wine-predictor:latest
```
DockerHub Push Screenshot: 
![Screenshot 2025-04-23 at 2 31 37 PM](https://github.com/user-attachments/assets/18094ab8-3909-4c68-b1ed-9925f1fccd2f)
























