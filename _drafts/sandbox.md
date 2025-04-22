---
layout: default
title: "Key-Value List"
data:
    - { Title: "Abdominal Aorto-iliac Artery Aneurysms (2024)", URL: "https://esvs.org/wp-content/uploads/2024/02/ESVS-2024-AAA-Guidelines.pdf" }
    - { Title: "Acute Limb Ischaemia (2020)", URL: "https://esvs.org/wp-content/uploads/2021/08/Acute-Limb-Ischaemia-Feb-2020.pdf" }
    - { Title: "Antithrombotic Therapy (2023)", URL: "https://esvs.org/wp-content/uploads/2023/09/Antithrombotic-Therapy-2023.pdf" }
    - { Title: "Aortic Arch Surgery (Position Paper) (2019)", URL: "https://esvs.org/wp-content/uploads/2021/08/Consensus-document-ESVS-EATCS-Aortic-Arch.pdf" }
    - { Title: "Atherosclerotic Carotid and Vertebral Artery Disease (2023)", URL: "https://esvs.org/wp-content/uploads/2022/10/2023-CPG-on-the-Management-of-Atherosclerotic-Carotid-and-Vertebral-Artery-Disease.pdf" }
    - { Title: "Chronic Venous Disease of the Lower Limbs (2022)", URL: "https://esvs.org/wp-content/uploads/2022/02/2022-CVD-guidelines-extensive-version-24.01.2022-1.pdf" }
    - { Title: "Chronic Limb-Threatening Ischemia (CLTI) (2019)", URL: "https://esvs.org/wp-content/uploads/2021/08/CLTI-Guidelines-ESVS-SVS-WFVS.pdf" }
    - { Title: "Descending Thoracic Aorta Diseases (2017)", URL: "https://esvs.org/wp-content/uploads/2021/08/Descending-Thoracic-Aorta-Diseases-2017.pdf" }
    - { Title: "Diseases of Mesenteric Arteries and Veins (2017)", URL: "https://esvs.org/wp-content/uploads/2021/08/Disease-of-Mesenteric-Arteries-and-Veins-2017.pdf" }
    - { Title: "Peripheral Arterial Disease (PAD) (2024)", URL: "https://esvs.org/wp-content/uploads/2024/01/PAD-2024-Guidelines.pdf" }
    - { Title: "Radiation Safety (2023)", URL: "https://esvs.org/wp-content/uploads/2023/09/Radiation-Safety-2023-Guidelines.pdf" }
    - { Title: "Vascular Access (2018)", URL: "https://esvs.org/wp-content/uploads/2021/08/Vascular-Access-2018.pdf" }
    - { Title: "Vascular Graft and Endograft Infections (2020)", URL: "https://esvs.org/wp-content/uploads/2021/08/Managemen-of-Vascular-Graft-and-Endograft-Infections-Mar-2020.pdf" }
    - { Title: "Venous Thrombosis (2021)", URL: "https://esvs.org/wp-content/uploads/2021/08/Venous-thrombosis-guidelines-2021-1.pdf" }
    - { Title: "Vascular Trauma (2025)", URL: "https://esvs.org/wp-content/uploads/2025/01/2025-Vascular-Trauma-Guidelines.pdf" }

---

### ESVS Clinical Practice Guidelines – Up-to-Date and Accessible

| Guideline Title |  
|-----------------|
{% for key in page.data %}
| [{{ key["Title"] | replace: "_", " " }}]({{ key["URL"] }}){:target="_blank"} |
{% endfor %}