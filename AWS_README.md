Configuring VPC to host our Smart Contracts on an EC2 instance
========================================

![image](https://user-images.githubusercontent.com/104800728/202856865-6949b6d5-9758-4034-aed3-c535528d45e0.png)

1. **Virtual Private Cloud (VPC)**- Enables you to launch AWS resources into a virtual network that you've defined.
2. **Availability Zone (AZ)**- Distinct locations within an AWS Region that are engineered to be isolated from failures in other Availability Zones.
3. **Subent**- A range of IP addresses in your VPC. (You can configure public and/or private subnets)
4. **Internet Gateway**- horizontally scaled, redundant, and highly available VPC component that allows communication between your VPC and the internet.
5. **Security Group**- Acts as a virtual firewall at the instance level controlling inbound and outbound traffic. They only have rules that allow traffic due to all trafic beiing dienied at first.
6. **Network Access Control List (NACL)**- Acts as a firewall at the subnet level. Traffic rules are determined by rule # starting from lowest to highest. AWS recommends adding Rules in increments of 10 so that you have room to add additional rules inbetween them if needed.
7. **Router**- The primary function of this VPC router is to take all of the route tables defined within that VPC, and then direct the traffic flow within that VPC, as well as to subnets outside of the VPC, based on the rules defined within those tables.

Logging into your EC2 Instance
--------------------------
1. Set up default VPC
2. Add EC2 instance to the **public subnet** and **public security group** with the default VPC. 
3. Specify which ports you are going to allow traffic through in the securty group.
4. Download your keys and then connect to EC2 Instance either using SSH or PUTTY. You can also set up a cloud9 environment. 
5. Now you can begn your installation process. 

Install
--------
1. First install node.js here: [Download - Node.js](https://nodejs.org/en/download/)
2. Next install:
```
pip install streamlit
sudo apt install python3-venv
pip install pandas
npm install web3
```
Running Your Streamlit Application
-----------------------------

1. Navigate to your application folder.
2. Navigate to the app.py folder.
3. Run ```streamlit app.py```
4. Copy the External URL and Paste it into your browser.

**Congrats!! Your Streamlit application is running on an EC2 Instance!!**


Deploy static wesites on AWS using S3, CloudFront, and Route53
===================================

![image](https://user-images.githubusercontent.com/104800728/202912500-77f15a3b-97e1-480f-8376-b2c4744e2c27.png)

S3 Bucket Setup
===============

Create a bucket & then add Object to bucket
---------------

Bucket names must conform with DNS requirements:

* Should not contain uppercase characters
* Should not contain underscores
* Should be between 3 and 63 characters long
* Should not end with a dash
* Cannot contain two, adjacent periods
* Cannot contain dashes next to periods (e.g., "my-.bucket.com" and "my.-bucket" are invalid)



Configure the Bucket Static Website Hosting
-------------------------------------------

<img width="1092" alt="Screen Shot 2022-11-19 at 9 32 15 AM" src="https://user-images.githubusercontent.com/104800728/202855977-dc768964-d2d6-4817-8e8f-d72ebf0c8b6e.png">

Once the bucket is created, select it and choose `Properties > Static Website Hosting`. 


Configure a Public Readable Policy for the Bucket
-------------------------------------------------

Static sites hosted on S3 do not support private files (password protection, etc). You must make all files publicly accessible. From your buckets `Properties` page, choose `Permissions > Edit/Add bucket policy`. Copy and past the policy below (replace **YOUR-BUCKET-NAME** for the bucketName you created previously)

```json
{
	"Version": "2008-10-17",
	"Statement": [
		{
			"Sid": "PublicReadForGetBucketObjects",
			"Effect": "Allow",
			"Principal": {
				"AWS": "*"
			},
			"Action": "s3:GetObject",
			"Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
		}
	]
}
```

User Permissions
----------------

From the [AWS IAM Users Console](https://console.aws.amazon.com/iam/?#users) select the newly created user, then the `Permissions` Tab, then click the `Attach User Policy` button.  Paste in the following (substituting BUCKET-NAME as appropriate).

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:DeleteObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Sid": "AllowNewUserAccessToMyBucket",
      "Resource": [
        "arn:aws:s3:::BUCKET-NAME",
		"arn:aws:s3:::BUCKET-NAME/*"
      ],
      "Effect": "Allow"
    }
  ]
}
```

Select the bucket you uploaded your file to. Next press copy URL.

<img width="1440" alt="Screen Shot 2022-11-19 at 9 42 44 AM" src="https://user-images.githubusercontent.com/104800728/202856514-809f4b64-dc7d-40a1-b011-fc79c5f2c727.png">

How to Configure CloudFront
=========================
1. Open the CloudFront page in the AWS console.Create Bucket Screen
2. Click the Create Distribution button. If you are asked to select a delivery method, choose Web and click Get Started
3. In the Origin Settings section, click on the Origin Domain Name and TYPE the bucket website URL from the bucket we just created. DO NOT select it from the dropdown. (The bucket URL is available in the static website hosting section of the S3 console.)
4. In the Default Cache Behavior Settings section, we need to change the Viewer Control Policy. Set this to Redirect HTTP to HTTPS. Leave everything else set to the defaults.
5. Click Create Distribution at the bottom of the page. This will take you back to the main CloudFront screen, where you will see a list of CloudFront distributions (the one we just created may be your only one). Notice that the status says In Progress. This means CloudFront is copying your content out to the edge locations. This may take a few moments. When it is done, the status will change to Deployed.
6. Now we have the S3 bucket serving your content, and we have it distributed on CloudFront. CloudFront creates a unique URL for your distribution. This can be found on the main CloudFront screen under the Domain Name column. It will look something like this:

<img width="1440" alt="Screen Shot 2022-11-19 at 9 30 15 AM" src="https://user-images.githubusercontent.com/104800728/202856080-8e6f5859-9ed0-443d-b4ba-4877bc352055.png">

How to Configure Route 53 and The Certificate Manager
===================================================


Results!
=======
