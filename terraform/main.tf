provider "aws" {
  region = "us-east-1"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  
  backend "s3" {
    bucket = "inventory-terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "inventory-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
  
  tags = {
    Environment = "production"
    Project     = "inventory"
  }
}

module "ecs" {
  source = "terraform-aws-modules/ecs/aws"
  
  cluster_name = "inventory-cluster"
  
  cluster_configuration = {
    execute_command_configuration = {
      logging = "OVERRIDE"
      log_configuration = {
        cloud_watch_log_group_name = "/aws/ecs/inventory"
      }
    }
  }
  
  fargate_capacity_providers = {
    FARGATE = {
      default_capacity_provider_strategy = {
        weight = 50
      }
    }
    FARGATE_SPOT = {
      default_capacity_provider_strategy = {
        weight = 50
      }
    }
  }
  
  tags = {
    Environment = "production"
    Project     = "inventory"
  }
}

module "alb" {
  source = "terraform-aws-modules/alb/aws"
  
  name = "inventory-alb"
  
  load_balancer_type = "application"
  vpc_id             = module.vpc.vpc_id
  subnets            = module.vpc.public_subnets
  security_groups    = [module.alb_sg.security_group_id]
  
  target_groups = [
    {
      name             = "inventory-tg"
      backend_protocol = "HTTP"
      backend_port     = 8000
      target_type      = "ip"
      health_check = {
        path                = "/health/"
        healthy_threshold   = 2
        unhealthy_threshold = 10
        interval            = 30
        timeout            = 5
      }
    }
  ]
  
  tags = {
    Environment = "production"
    Project     = "inventory"
  }
}

module "ecr" {
  source = "terraform-aws-modules/ecr/aws"
  
  repository_name = "inventory-app"
  repository_type = "private"
  
  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 30 images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 30
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
  
  tags = {
    Environment = "production"
    Project     = "inventory"
  }
}

module "alb_sg" {
  source = "terraform-aws-modules/security-group/aws"
  
  name        = "inventory-alb-sg"
  description = "Security group for ALB"
  vpc_id      = module.vpc.vpc_id
  
  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "https-443-tcp"]
  
  egress_rules = ["all-all"]
  
  tags = {
    Environment = "production"
    Project     = "inventory"
  }
}

module "ecs_sg" {
  source = "terraform-aws-modules/security-group/aws"
  
  name        = "inventory-ecs-sg"
  description = "Security group for ECS tasks"
  vpc_id      = module.vpc.vpc_id
  
  ingress_with_source_security_group_id = [
    {
      from_port                = 8000
      to_port                  = 8000
      protocol                 = "tcp"
      source_security_group_id = module.alb_sg.security_group_id
    }
  ]
  
  egress_rules = ["all-all"]
  
  tags = {
    Environment = "production"
    Project     = "inventory"
  }
} 