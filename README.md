# HealthTAG open-source FHIR node for hospital
Docker Compose to setup HIS base on FHIR with KONG as authentication layer

ไฟล์ Docker compose สำหรับการตั้ง HIS base on FHIR with KONG as authentication layer

# การใช้งาน 
## Requirements
1. Docker

## ขั้นตอนการติดตั้ง
1. Clone repository
2. `docker compose pull` จากนั้น `docker compose up -d`

## ขั้นตอนการใช้งาน
**สามารถอ่านคู่มือได้ที่** [https://healthtag.io/support](https://healthtag.io/support)
### การนำไฟล์ CSOP / 43 แฟ้ม เข้า
1. ไปที่ [http://localhost:8081](http://localhost:8081)
2. ทำการสร้างงาน แล้วอัพโหลดไฟล์ที่ระบบลองรับ
3. รอ Script ทำงาน
4. สามารถดูผลลัพธ์ได้ทาง Web Interface

### การเข้า FHIR Server
1. ไปที่ [http://localhost:8080/fhir](http://localhost:8080/fhir)

# Created by / สร้างโดย
- [Suttisak, MD. นพ.สุทธิศักดิ์](https://doctortons.com)
- [Wara, วรา](https://github.com/BabyThor)
