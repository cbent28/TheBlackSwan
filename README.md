# TheBlackSwan
![depix-mask](https://user-images.githubusercontent.com/104800728/201481962-9e6826c2-1af6-4297-a310-69b982994b5d.png)

Deploy static sites AWS an S3 Bucket using CloudFront and Route53
===================================

![image](https://user-images.githubusercontent.com/104800728/202855601-f119c4df-ad2e-407c-9239-beaf4ac98790.png)

S3 Bucket Setup
===============

<img width="1440" alt="Screen Shot 2022-11-17 at 12 49 31 PM" src="https://user-images.githubusercontent.com/104800728/202520500-2f9c26c6-b7de-4ae0-a084-7aadb5257f7a.png">

Create a bucket 
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

![Screen Shot 2022-11-17 at 1 13 05 PM](https://user-images.githubusercontent.com/104800728/202525712-9847e5ff-9da4-416f-8b9f-94bb862a031c.png)

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

S3 User Setup
=============

Log into your [AWS Console](https://console.aws.amazon.com/iam/?#users) and go to the [Users](https://console.aws.amazon.com/iam/?#users) management console. Click the `Create New Users` button and enter a username. 

Credentials File
----------------

Have AWS create a new key pair for the user and copy the contents into a `aws-credentials.json` file in the root directory of your project. You should add this file to `.gitignore` (or similar) so that credentials are not checked into version control.

```json
{ 
	"accessKeyId": "PUBLIC_KEY", 
	"secretAccessKey": "SECRET_KEY", 
	"region": "us-west-2" 
}
```

**note**: As AWS SDK's documentation points out, you could also set those as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables 

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
Results!
=======
Select the bucket you uploaded your file to. Next press copy URL.

![Screen Shot 2022-11-17 at 1 11 41 PM](https://user-images.githubusercontent.com/104800728/202526573-a7976c99-eff9-458b-b70f-426997c05a2c.png)
