resource "aws_iam_role_policy" "file_injection_invoker_policy" {
  name = "file_injection_invoker_policy"
  role = aws_iam_role.file_injection_invoker_role.id

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = file("iam/file_injection_invoker_policy.json")
}

resource "aws_iam_role" "file_injection_invoker_role" {
  name = "file_injection_invoker_role"

  assume_role_policy = file("iam/file_injection_invoker_role.json")
}
