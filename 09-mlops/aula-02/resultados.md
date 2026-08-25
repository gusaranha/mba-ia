
### local
```
gustavoaranha@Gustavos-iMac aula-02 % cd local/
gustavoaranha@Gustavos-iMac local % terraform init
Initializing the backend...

Initializing provider plugins...
- Reusing previous version of hashicorp/local from the dependency lock file
- Installing hashicorp/local v2.9.0...
- Installed hashicorp/local v2.9.0 (signed by HashiCorp)

Terraform has made some changes to the provider dependency selections recorded
in the .terraform.lock.hcl file. Review those changes and commit them to your
version control system if they represent changes you intended to make.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                             
If you ever set or change modules or backend configuration for Terraform,                                                                                                                                                                                    
rerun this command to reinitialize your working directory. If you forget, other                                                                                                                                                                              
commands will detect it and remind you to do so if necessary.                                                                                                                                                                                                
gustavoaranha@Gustavos-iMac local % terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # local_file.Ola_Mundo will be created
  + resource "local_file" "Ola_Mundo" {
      + content              = "Olá, Mundo Terraform!"
      + content_base64sha256 = (known after apply)
      + content_base64sha512 = (known after apply)
      + content_md5          = (known after apply)
      + content_sha1         = (known after apply)
      + content_sha256       = (known after apply)
      + content_sha512       = (known after apply)
      + directory_permission = "0777"
      + file_permission      = "0777"
      + filename             = "./ola.txt"
      + id                   = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

local_file.Ola_Mundo: Creating...
local_file.Ola_Mundo: Creation complete after 0s [id=e1d7d1ffb9c14aaf72ed68dec665c48bd465b743]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

### exemplo-credenciais
```
gustavoaranha@Gustavos-iMac exemplo-credenciais % terraform init && terraform apply 
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/local versions matching "~> 2.0"...
- Finding hashicorp/random versions matching "~> 3.0"...
- Installing hashicorp/random v3.9.0...
- Installed hashicorp/random v3.9.0 (signed by HashiCorp)
- Installing hashicorp/local v2.9.0...
- Installed hashicorp/local v2.9.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see                                                                                                                                                                                
any changes that are required for your infrastructure. All Terraform commands                                                                                                                                                                                
should now work.                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                             
If you ever set or change modules or backend configuration for Terraform,                                                                                                                                                                                    
rerun this command to reinitialize your working directory. If you forget, other                                                                                                                                                                              
commands will detect it and remind you to do so if necessary.                                                                                                                                                                                                

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # local_sensitive_file.credenciais will be created
  + resource "local_sensitive_file" "credenciais" {
      + content              = (sensitive value)
      + content_base64sha256 = (known after apply)
      + content_base64sha512 = (known after apply)
      + content_md5          = (known after apply)
      + content_sha1         = (known after apply)
      + content_sha256       = (known after apply)
      + content_sha512       = (known after apply)
      + directory_permission = "0700"
      + file_permission      = "0700"
      + filename             = "./credenciais.txt"
      + id                   = (known after apply)
    }

  # random_password.senha will be created
  + resource "random_password" "senha" {
      + bcrypt_hash = (sensitive value)
      + id          = (known after apply)
      + length      = 16
      + lower       = true
      + min_lower   = 0
      + min_numeric = 0
      + min_special = 0
      + min_upper   = 0
      + number      = true
      + numeric     = true
      + result      = (sensitive value)
      + special     = true
      + upper       = true
    }

  # random_pet.usuario will be created
  + resource "random_pet" "usuario" {
      + id        = (known after apply)
      + length    = 2
      + separator = "_"
    }

Plan: 3 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + usuario_gerado = (known after apply)

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

random_pet.usuario: Creating...
random_password.senha: Creating...
random_pet.usuario: Creation complete after 0s [id=flowing_yak]
random_password.senha: Creation complete after 0s [id=none]
local_sensitive_file.credenciais: Creating...
local_sensitive_file.credenciais: Creation complete after 0s [id=117a445a8c207389ea9614693867af51c46d7d0c]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.                                                                                                                                                                                                  

Outputs:                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                             
usuario_gerado = "flowing_yak"         
```

### exemplo-docker
```
gustavoaranha@Gustavos-iMac exemplo-docker % terraform init && terraform apply 
Initializing the backend...

Initializing provider plugins...
- Reusing previous version of kreuzwerker/docker from the dependency lock file
- Using previously-installed kreuzwerker/docker v3.9.0


Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see                                                                                                                                                                                
any changes that are required for your infrastructure. All Terraform commands                                                                                                                                                                                
should now work.                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                             
If you ever set or change modules or backend configuration for Terraform,                                                                                                                                                                                    
rerun this command to reinitialize your working directory. If you forget, other                                                                                                                                                                              
commands will detect it and remind you to do so if necessary.                                                                                                                                                                                                
docker_image.nginx: Refreshing state... [id=sha256:8541484afbc9c8a5a8a99b379568ebbc957f658583ec9448fc43104229c03cf8nginx:latest]
docker_container.site: Refreshing state... [id=e2e9f3746e63f0acb3f3a72812c49379fcbd41122339a1a021b36244526f6c21]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # docker_container.site will be created
  + resource "docker_container" "site" {
      + attach                                      = false
      + bridge                                      = (known after apply)
      + command                                     = (known after apply)
      + container_logs                              = (known after apply)
      + container_read_refresh_timeout_milliseconds = 15000
      + entrypoint                                  = (known after apply)
      + env                                         = (known after apply)
      + exit_code                                   = (known after apply)
      + hostname                                    = (known after apply)
      + id                                          = (known after apply)
      + image                                       = "sha256:8541484afbc9c8a5a8a99b379568ebbc957f658583ec9448fc43104229c03cf8"
      + init                                        = (known after apply)
      + ipc_mode                                    = (known after apply)
      + log_driver                                  = (known after apply)
      + logs                                        = false
      + memory_reservation                          = 0
      + must_run                                    = true
      + name                                        = "meu-site-local"
      + network_data                                = (known after apply)
      + network_mode                                = "bridge"
      + read_only                                   = false
      + remove_volumes                              = true
      + restart                                     = "no"
      + rm                                          = false
      + runtime                                     = (known after apply)
      + security_opts                               = (known after apply)
      + shm_size                                    = (known after apply)
      + start                                       = true
      + stdin_open                                  = false
      + stop_signal                                 = (known after apply)
      + stop_timeout                                = (known after apply)
      + tty                                         = false
      + wait                                        = false
      + wait_timeout                                = 60

      + healthcheck (known after apply)

      + labels (known after apply)

      + ports {
          + external = 8080
          + internal = 80
          + ip       = "0.0.0.0"
          + protocol = "tcp"
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

docker_container.site: Creating...
docker_container.site: Creation complete after 1s [id=e8e6f881664cb0b3cbe769c4df7086cc5e052d7448538f6ce29766e521e134d5]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.                                                                                                                                                                                                  

Outputs:                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                             
acesse_em = "http://localhost:8080"   
```

### exemplo-ssh
```
gustavoaranha@Gustavos-iMac exemplo-ssh % terraform init && terraform apply 
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/tls versions matching "~> 4.0"...
- Finding hashicorp/local versions matching "~> 2.0"...
- Installing hashicorp/tls v4.3.0...
- Installed hashicorp/tls v4.3.0 (signed by HashiCorp)
- Installing hashicorp/local v2.9.0...
- Installed hashicorp/local v2.9.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see                                                                                                                                                                                
any changes that are required for your infrastructure. All Terraform commands                                                                                                                                                                                
should now work.                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                             
If you ever set or change modules or backend configuration for Terraform,                                                                                                                                                                                    
rerun this command to reinitialize your working directory. If you forget, other                                                                                                                                                                              
commands will detect it and remind you to do so if necessary.                                                                                                                                                                                                

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # local_file.chave_privada will be created
  + resource "local_file" "chave_privada" {
      + content              = (sensitive value)
      + content_base64sha256 = (known after apply)
      + content_base64sha512 = (known after apply)
      + content_md5          = (known after apply)
      + content_sha1         = (known after apply)
      + content_sha256       = (known after apply)
      + content_sha512       = (known after apply)
      + directory_permission = "0777"
      + file_permission      = "0600"
      + filename             = "./id_rsa"
      + id                   = (known after apply)
    }

  # local_file.chave_publica will be created
  + resource "local_file" "chave_publica" {
      + content              = (known after apply)
      + content_base64sha256 = (known after apply)
      + content_base64sha512 = (known after apply)
      + content_md5          = (known after apply)
      + content_sha1         = (known after apply)
      + content_sha256       = (known after apply)
      + content_sha512       = (known after apply)
      + directory_permission = "0777"
      + file_permission      = "0777"
      + filename             = "./id_rsa.pub"
      + id                   = (known after apply)
    }

  # tls_private_key.chave will be created
  + resource "tls_private_key" "chave" {
      + algorithm                     = "RSA"
      + ecdsa_curve                   = "P224"
      + id                            = (known after apply)
      + private_key_openssh           = (sensitive value)
      + private_key_pem               = (sensitive value)
      + private_key_pem_pkcs8         = (sensitive value)
      + public_key_fingerprint_md5    = (known after apply)
      + public_key_fingerprint_sha256 = (known after apply)
      + public_key_openssh            = (known after apply)
      + public_key_pem                = (known after apply)
      + rsa_bits                      = 4096
    }

Plan: 3 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + fingerprint = (known after apply)

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tls_private_key.chave: Creating...
tls_private_key.chave: Creation complete after 1s [id=b5a9d6203e847bce87f296717aea90bff1d39f9e]
local_file.chave_publica: Creating...
local_file.chave_privada: Creating...
local_file.chave_publica: Creation complete after 0s [id=f7499c2938d44633c463b8b718f1f997d04dbb71]
local_file.chave_privada: Creation complete after 0s [id=5f79e479b6b69b803cc9b06e1b2d5c8ba7958e21]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.                                                                                                                                                                                                  

Outputs:                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                             
fingerprint = "SHA256:yXWa3sawjrtyhjwVRt1zNdVJm/qkwn50TsrchVQ6vLM"  
```

### exemplo-zip
```
gustavoaranha@Gustavos-iMac exemplo-zip % terraform init && terraform apply 
Initializing the backend...

Initializing provider plugins...
- terraform.io/builtin/terraform is built in to Terraform
- Finding hashicorp/archive versions matching "~> 2.0"...
- Installing hashicorp/archive v2.8.0...
- Installed hashicorp/archive v2.8.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see                                                                                                                                                                                
any changes that are required for your infrastructure. All Terraform commands                                                                                                                                                                                
should now work.                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                             
If you ever set or change modules or backend configuration for Terraform,                                                                                                                                                                                    
rerun this command to reinitialize your working directory. If you forget, other                                                                                                                                                                              
commands will detect it and remind you to do so if necessary.                                                                                                                                                                                                
data.archive_file.pacote: Reading...
data.archive_file.pacote: Read complete after 0s [id=aaee80884a730f847fc7d45af1b5da36060ffd62]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # terraform_data.info will be created
  + resource "terraform_data" "info" {
      + id     = (known after apply)
      + input  = "aaee80884a730f847fc7d45af1b5da36060ffd62"
      + output = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + sha256_do_pacote = "aaee80884a730f847fc7d45af1b5da36060ffd62"

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

terraform_data.info: Creating...
terraform_data.info: Provisioning with 'local-exec'...
terraform_data.info (local-exec): Executing: ["/bin/sh" "-c" "echo 'Pacote gerado em ./app.zip — 176 bytes'"]
terraform_data.info (local-exec): Pacote gerado em ./app.zip — 176 bytes
terraform_data.info: Creation complete after 0s [id=9edd25b8-78f9-16dd-e9be-dbcffdda5010]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.                                                                                                                                                                                                  

Outputs:                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                             
sha256_do_pacote = "aaee80884a730f847fc7d45af1b5da36060ffd62"      
```