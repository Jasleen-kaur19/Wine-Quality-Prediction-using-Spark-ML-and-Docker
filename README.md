# Wine-Quality-Prediction-using-Spark-ML-and-Docker

## Wine Quality Prediction using Spark ML and Docker

This project implements a distributed machine learning system for wine quality prediction using Apache Spark ML on AWS EC2 instances. It includes training and prediction components, and is containerized with Docker for easy deployment.

---

## 📦 Dockerhub Repository

**Dockerhub Repo**: [jasleen4499/wine-predictor](https://hub.docker.com/r/jasleen4499/wine-predictor)

You can pull the Docker image using:
```bash
docker pull jasleen4499/wine-predictor:latest
```

🚀 Project Architecture

Step	Details
1	Launch 4 EC2 instances (1 Master + 3 Workers)
2	Install and Configure Java, Hadoop, and Spark
3	SSH Key setup for password-less communication
4	Start Spark Master and Worker nodes
5	Train the model on Spark cluster
6	Build Docker image for prediction
7	Push Docker image to Dockerhub
8	Run the model prediction inside Docker container
☁️ Launch EC2 Instances
Instance Type: t2.large

Total Instances: 4 (1 Master + 3 Workers)

VPC: All instances should be in the same VPC and subnet.

Screenshot: (Add your screenshot here)

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
Cluster Running Screenshot:
(Add your screenshot here)
```
📂 Upload Dataset
Upload datasets to all nodes:
```bash
scp -i "your-key.pem" TrainingDataset.csv ec2-user@<instance-public-ip>:~/
scp -i "your-key.pem" ValidationDataset.csv ec2-user@<instance-public-ip>:~/
```
🧠 Train the Model
Submit Spark job:
```bash
spark-submit --master spark://<Master-Private-IP>:7077 wine-train.py
```
Training Result:

F1 Score: 0.5610

Accuracy: 57.5%

Screenshot:
(Add your screenshot here)

🐳 Build Docker Image
Build the Docker image:
```bash
docker build -t wine-predictor .
```
Screenshot:
(Add your screenshot here)

Run the Docker container:
```bash
docker run wine-predictor
```

Prediction Output:
(Add your output screenshot here)

Push Docker image to Dockerhub:
```bash
docker push jasleen4499/wine-predictor:latest
```
DockerHub Push Screenshot:
(Add your DockerHub push screenshot here)

📈 Results

Metric	Value
F1 Score	0.561
Accuracy	57.5%
Example Output:

label	prediction
5.0	5.0
5.0	5.0
6.0	6.0
5.0	5.0
