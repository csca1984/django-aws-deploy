resource "aws_ecr_repository" "django_app" {
  name                 = "django-app"
  image_tag_mutability = "MUTABLE"

  tags = local.common_tags
}
