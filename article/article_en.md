# LINE Bot

## LINE

### Provider

### Channel

|Key|Value|
|:--|:--|
|Channel Type|Messaging API|
|Provider| *ProviderName* |
|Channel name|TextractBot|
|Channel description|LINE Bot for Text Extraction from Image|
|Category| *(Any you want)* |
|Subcategory| *(Any you want)* |
|Email address| *You Email Address* |


## Secret

## IAM Policy 

Policy Name : ``

## S3 Bucket

Bucket Name: `yamagishihrd-artifacts`

## Install Libraries

## Package


```
% aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket yamagishihrd-artifacts \
    --output-template-file artifacts/packaged-template.yaml
```

## Deploy

```
% aws cloudformation deploy \
    --template-file artifacts/packaged-template.yaml \
    --stack-name cf-stack-textractbot \
    --capabilities CAPABILITY_IAM
```

---
EOF
