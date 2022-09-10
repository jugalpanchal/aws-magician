locals {
  lambda_zip_location =  "outputs/file_injection_invoker_payload.zip"
}

# Archive a single file.
data "archive_file" "file_injection_invoker_payload" {
  type        = "zip"
  source_file = "file_injection_invoker_handler.py"
  output_path = local.lambda_zip_location
}

resource "aws_lambda_function" "test_lambda" {
  filename      = local.lambda_zip_location
  function_name = "file_injection_invoker"
  role          = aws_iam_role.file_injection_invoker_role.arn
  handler       = "file_injection_invoker_handler.setup"

  # If there is any file change then it gets deployed, otherwise it is not required.
  source_code_hash = filebase64sha256(local.lambda_zip_location)

  runtime = "python3.8"

  environment {
    variables = {
      sandbox_url = "https:something_ok"
    }
  }
}
