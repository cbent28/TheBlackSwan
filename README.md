# TheBlackSwan

Black Swan and explanation goes here!!

Configruing VPC to host our Smart Contracts on an EC2
========================================

![image](https://user-images.githubusercontent.com/104800728/202856865-6949b6d5-9758-4034-aed3-c535528d45e0.png)

1. AWS Virtual Private Cloud- 
2. Availability Zone (AZ)- 
3. Subent- 
4. Internet Gateway- 
5. Security Group-
6. Network Access Control List (NACL)- 
7. Router- 

Deploy static sites AWS an S3 Bucket using CloudFront and Route53
===================================

![image](https://user-images.githubusercontent.com/104800728/202855601-f119c4df-ad2e-407c-9239-beaf4ac98790.png)

S3 Bucket Setup
===============

Create a bucket & then add Object to bucket
---------------

Bucket names must conform with DNS requirements:

* **Should not contain uppercase characters**
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

Results!
=======
