#!/bin/bash

# Configuración inicial
INSTANCE_TYPE="t2.micro"
KEY_NAME="etf-key"
SECURITY_GROUP="etf-sg"
AMI_ID="ami-08c40ec9ead489470"  # Ubuntu 22.04 LTS

# Crear instancia EC2
echo "Creando instancia EC2..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-groups $SECURITY_GROUP \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=etf-sp500-analysis}]' \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "Instancia $INSTANCE_ID creada"

# Esperar a que la instancia esté running
echo "Esperando a que la instancia esté disponible..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Obtener IP pública
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "Instancia disponible en $PUBLIC_IP"

# Configurar acceso SSH
echo "Configurando acceso SSH..."
ssh -i ~/.ssh/$KEY_NAME.pem ubuntu@$PUBLIC_IP <<EOF
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y python3-pip python3-venv mongodb
  git clone https://github.com/tu-usuario/etf-sp500-bigdata-project.git
  cd etf-sp500-bigdata-project
  python3 -m venv etfenv
  source etfenv/bin/activate
  pip install -r requirements.txt
EOF

echo "Despliegue completado. Accede con:"
echo "ssh -i ~/.ssh/$KEY_NAME.pem ubuntu@$PUBLIC_IP"