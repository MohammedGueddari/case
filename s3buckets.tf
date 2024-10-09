resource "aws_s3_bucket" "raw_bucket" {
    bucket = "namebucketname-accountid"
    tags = {
      key = ""
    }
  
}

resource "aws_s3_bucket_ownership_controls" "s3_bucket_acl_ownership" {
    bucket = aws_glue_trigger.TriggerJobIni
    rule {
      object_ownership = "ObjectWriter"
    }
    depends_on = [ aws_glue_trigger.TriggerJobIni ]
  
}

resource "aws_s3_bucket_acl" "acl" {
    bucket = aws_s3_bucket.raw_bucket.bucket
    acl = "private"
    depends_on = [ aws_glue_trigger.TriggerJobIni, aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership ]
}

resource "aws_s3_bucket_public_access_block" "bucket_public_access_block" {
    bucket = aws_glue_trigger.TriggerJobIni
    ignore_public_acls = true
    block_public_acls = true
    block_public_policy = true
    restrict_public_buckets = true
    depends_on = [ aws_glue_trigger.TriggerJobIni ]
  
}

data "aws_kms_key" "kms_key" {
    key_id = "alias/kms"
  
}

data "aws_iam_policy_document" "bucket_policy" {
    statement {
      sid = "AllowBucket"
      principals {
        type = "AWS"
        identifiers = ["arn:aws:iam::${data.aws_caller_identity.current}:root"]
      }
      effect = "Allow"
      actions = [
        "s3:GetObject",
        "s3:GetObjectVersion"
      ]
      resources = [
        "arn:aws:s3:::bucketname/*",
        "arn:aws:s3:::bucketname"
      ]
    }
    statement {
      sid = "AllowSSLRequestOnly"
      principals {
        type = "*"
        identifiers = ["*"]
      }
      effect = "Deny"
      actions = [
        "s3:*"
      ]
      resources = [
        "arn:aws:s3:::bucketname/*",
        "arn:aws:s3:::bucketname"
      ]
      condition {
        test = "Bool"
        variable = "aws:SecureTransport"
        values = ["false"]
      }
    }
  
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_encryption" {
    bucket = aws_glue_trigger.TriggerJobIni
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = data.aws_kms_key.kms_key
        sse_algorithm = "aws:kms"
      }
      bucket_key_enabled = true
    }
    depends_on = [ aws_glue_trigger.TriggerJobIni ]
  
}

resource "aws_s3_bucket_policy" "policy" {
    bucket = aws_glue_trigger.TriggerJobIni
    policy = data.aws_iam_policy_document.bucket_policy
    depends_on = [ aws_glue_trigger.TriggerJobIni ]
  
}

resource "aws_s3_bucket_versioning" "versioning" {
    bucket = aws_glue_trigger.TriggerJobIni
    versioning_configuration {
      status = "Disabled"
    }
    depends_on = [ aws_glue_trigger.TriggerJobIni ]
  
}
resource "aws_s3_bucket_lifecycle_configuration" "lifecycle" {
    bucket = aws_glue_trigger.TriggerJobIni
    rule {
      id = "Lifecycle"
      status = "Enabled"
      expiration {
        days = "365"
      }
    }
    depends_on = [ aws_glue_trigger.TriggerJobIni ]
}

