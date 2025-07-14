variable "project_id" {
  type        = string
  description = "ID del proyecto de GCP"
}
variable "region" {
  default = "us-central1"
}
variable "service_name" {
  default = "delayfly"
}
variable "container_register" {
  default = "us-central1-docker.pkg.dev"
}
variable "repo_name" {
  default = "ml-models"
}
variable "image_name" {
  default = "mldelay"
}
variable "image_tag" {
  default = "latest"
}
variable "container_concurrency" {
  default = 20
}
variable "min_instances" {
  default = 0
}
variable "max_instances" {
  default = 1
}
