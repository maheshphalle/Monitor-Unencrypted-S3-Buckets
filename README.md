# Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3

## **Project Overview**
This project automates the detection of unencrypted S3 buckets using an **AWS Lambda function** with **Boto3 (AWS SDK for Python)**. The function lists all S3 buckets in an AWS account and identifies those that do not have **server-side encryption (SSE)** enabled.

## **Features**
✔ Detects all S3 buckets in the AWS account.  
✔ Checks if server-side encryption is enabled.  
✔ Logs the names of unencrypted buckets.  
✔ Can be extended to send notifications (e.g., AWS SNS, Email).  

---

## **1️⃣ Prerequisites**
Before running this project, ensure you have:

- ✅ An **AWS Account**.
- ✅ An IAM role with **`AmazonS3ReadOnlyAccess`** permission.
- ✅ An **S3 bucket** with and without encryption for testing.
- ✅ Python **3.x** installed (for local testing).
- ✅ AWS CLI installed and configured (`aws configure`).

---

## **2️⃣ AWS Setup Steps**

### **Step 1: Create IAM Role for Lambda**
1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/).
2. Click **Roles** → **Create Role**.
3. Choose **AWS Service** → Select **Lambda**.
4. Attach **AmazonS3ReadOnlyAccess** policy.
5. Name the role: `maheshS3MonitorRole`.
6. Click **Create Role**.

---

### **Step 2: Create an AWS Lambda Function**
1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Click **Create Function** → Choose **Author from Scratch**.
3. Name it: `maheshS3MonitorUnencryptedBuckets`.
4. Choose **Python 3.x** as the runtime.
5. Assign the IAM Role **maheshS3MonitorRole**.
6. Click **Create Function**.

---

### **Step 3: Deploy the Python Script**
1. Open the Lambda function editor.
2. Replace the default script with:

```python
import boto3

def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    
    try:
        response = s3_client.list_buckets()
        unencrypted_buckets = []

        for bucket in response["Buckets"]:
            bucket_name = bucket["Name"]
            try:
                encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
            except Exception as e:
                if "ServerSideEncryptionConfigurationNotFoundError" in str(e):
                    unencrypted_buckets.append(bucket_name)
        
        if unencrypted_buckets:
            print(f"Unencrypted S3 Buckets Found: {unencrypted_buckets}")
        else:
            print("All buckets have encryption enabled.")

    except Exception as e:
        print(f"Error listing buckets: {e}")
```

3. Click **Deploy**.

---

### **Step 4: Test the Function**
1. Click **Test** → Create a new test event.
2. Enter any event data (not required for this function).
3. Click **Run**.
4. Check the **logs in CloudWatch** for unencrypted bucket names.

---

## **3️⃣ Expected Output**
If unencrypted buckets exist, you'll see:
```
Unencrypted S3 Buckets Found: ['mahesh-unencrypted-bucket1']
```
If all buckets have encryption enabled:
```
All buckets have encryption enabled.
```

---

## **4️⃣ How to Run Locally**
1. Install Boto3:
   ```bash
   pip install boto3
   ```
2. Set up AWS CLI:
   ```bash
   aws configure
   ```
3. Run the script:
   ```bash
   python monitor_s3_encryption.py
   ```

---

## **5️⃣ Enhancements**
📌 Send alerts via **AWS SNS** or **Email**.  
📌 Store logs in **Amazon CloudWatch**.  
📌 Automate execution using **AWS EventBridge** (CloudWatch Events).  

---

## **7️⃣ License**
This project is open-source under the MIT License.

---

## **8️⃣ Author**
👨‍💻 Developed by **Mahesh**  


