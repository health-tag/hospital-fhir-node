 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import xmltodict
import json
import requests
import glob

tran_items = {}
disp_items = {}
detail_items = {}

base_fhir_url = 'http://hapi-fhir-jpaserver-start:8080/fhir'

license_mapping = {
    'ว': {
        'type': 'MD',
        'system': 'https://www.tmc.or.th'
    },
    'ท': {
        'type': 'DDS',
        'system': 'https://www.dentalcouncil.or.th'
    },
    'พ': {
        'type': 'NP',
        'system': 'https://www.tnmc.or.th'
    },
    'ภ': {
        'type': 'RPH',
        'system': 'https://www.pharmacycouncil.org'
    }
}

disp_status_mapping = {
    '0': 'cancelled',
    '1': 'completed',
    '2': 'declined',
    '3': 'entered-in-error'
}

prd_code_flag = {
    '0': False,
    '1': False,
    '2': True,
    '3': True,
    '4': False,
    '5': True,
    '6': True,
    '7': False,
    '8': False,
    '9': False,
}

bill_muad_mapping = {
    "1": "https://sil-th.org/CSOP/standardCode",
    "2": "https://sil-th.org/CSOP/standardCode",
    "3": "https://tmt.this.or.th",
    "5": "https://sil-th.org/CSOP/standardCode",
    "6": "https://tmlt.this.or.th",
    "7": "https://tmlt.this.or.th",
    "8": "https://sil-th.org/CSOP/standardCode",
    "9": "https://sil-th.org/CSOP/standardCode",
    "A": "https://sil-th.org/CSOP/standardCode",
    "B": "https://sil-th.org/CSOP/standardCode",
    "C": "https://sil-th.org/CSOP/standardCode",
    "D": "https://sil-th.org/CSOP/standardCode",
    "E": "https://sil-th.org/CSOP/standardCode",
    "F": "https://sil-th.org/CSOP/standardCode",
    "G": "https://sil-th.org/CSOP/standardCode",
    "H": "https://sil-th.org/CSOP/standardCode",
    "I": "https://sil-th.org/CSOP/standardCode",
}

files = glob.glob("./uploads/*")
bill_trans = ''
bill_disp = ''
for file in files:
    if 'BILLTRAN' in file:
        bill_trans = file
    elif 'BILLDISP' in file:
        bill_disp = file

with open(bill_trans, encoding="utf8") as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    h_code = data_dict['ClaimRec']['Header']['HCODE']
    h_name = data_dict['ClaimRec']['Header']['HNAME']
    bill_trans = data_dict['ClaimRec']['BILLTRAN'].split('\n')
    bill_trans_items = data_dict['ClaimRec']['BillItems'].split('\n')
    for item in bill_trans:
        item_split = item.split('|')
        item_data = {
            'station': item_split[0],
            'inv_no': item_split[4],
            'hn': item_split[6],
            'member_no': item_split[7],
            'pid': item_split[12],
            'name': item_split[13],
            'pay_plan': item_split[15],
            'items': []
        }
        tran_items[item_data['inv_no']] = item_data
    # for item in bill_trans_items:
    #     item_split = item.split('|')
    #     inv_no = item_split[0]
    #     item_da = {
    #         'sv_date': item_split[1],
    #         'bill_muad': item_split[2],
    #         'lc_code': item_split[3],
    #         'std_code': item_split[4],
    #         'desc': item_split[5],
    #         'qty': item_split[6],
    #         'up': item_split[7],
    #         'charge_amt': item_split[8],
    #         'charge_up': item_split[9],
    #         'claim_amt': item_split[10],
    #         'claim_cat': item_split[12],
    #     }
    #     items = tran_items[inv_no]
    #     items.append(item_da)
    #     tran_items[inv_no] = items

with open(bill_disp, encoding="utf8") as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    main_disps = data_dict['ClaimRec']['Dispensing'].split('\n')
    detail_disps = data_dict['ClaimRec']['DispensedItems'].split('\n')
    for item in main_disps:
        item_split = item.split('|')
        item_data = {
            'provider_id': item_split[0],
            'disp_id':item_split[1],
            'inv_no': item_split[2],
            'presc_date': item_split[5],
            'disp_date': item_split[6],
            'license_id': item_split[7],
            'disp_status': item_split[15],
            'practitioner': license_mapping[item_split[7][0]]
        }
        disp_items[item_data['disp_id']] = item_data
    for item in detail_disps:
        item_split = item.split('|')
        item_data = {
            'disp_id':item_split[0],
            'product_cat': item_split[1],
            'local_drug_id': item_split[2],
            'standard_drug_id': item_split[3],
            'dfs': item_split[5],
            'package_size': item_split[6],
            'instruction_code': item_split[7],
            'instruction_text': item_split[8],
            'quantity': item_split[9],
            # 'prd_code': item_split[14],
            # 'multiple_disp': item_split[17],
            # 'supply_for': item_split[18],
        }
        detail_items[item_data['disp_id']] = item_data

combined_data = {}
for disp_id, item in detail_items.items():
    combined_data = {
        **item,
        **disp_items[disp_id],
        **tran_items[disp_items[disp_id]['inv_no']]
    }
    patient_identifiers = [
        {
            "system": "https://www.dopa.go.th",
            "value": f"{combined_data['pid']}"
        },
        {
            "system": "https://sil-th.org/CSOP/hn",
            "value": f"{combined_data['hn']}"
        },
        # {
        #     "system": "https://healthtag.io",
        #     "value": "12345678"
        # } 
    ]
    if combined_data['member_no'] != '':
        patient_identifiers.append({
            "system": "https://sil-th.org/CSOP/memberNo",
            "value": f"{combined_data['member_no']}"
        })
    sequence = 1
    claim_items = []
    for bill_trans_item in combined_data['items']:
        bill_item = {
            "sequence": sequence,
            "category": {
                "coding": [
                    {
                        "system": "https://sil-th.org/fhir/CodeSystem/csop-billMuad",
                        "code": f"{bill_trans_item['bill_muad']}"
                    }
                ]
            },
            "productOrService": {
                "coding": [
                    {
                        "system": "https://sil-th.org/CSOP/localCode",
                        "code": f"{bill_trans_item['lc_code']}"
                    },
                    {
                        "system": "!?<<BILLTRAN.BillItems.BillMuad:System>>",
                        "code": f"{bill_trans_item['std_code']}"
                    }
                ],
                "text":f"{bill_trans_item['desc']}"
            },
            "modifier": [
                {
                    "coding": [
                        {
                            "system": "https://sil-th.org/fhir/CodeSystem/csop-claimCont",
                            "code": f"<<BILLDISP.DispensingItems.ClaimCont>>"
                        }
                    ]
                }
            ],
            "programCode": [
                {
                    "coding": [
                        {
                            "system": "https://sil-th.org/fhir/CodeSystem/csop-claimCat",
                            "code": f"{bill_trans_item['claim_cat']}"
                        }
                    ]
                }
            ],
            "servicedDate": f"{bill_trans_item['sv_date']}",
            "quantity": {
                "value": bill_trans_item['qty']
            },
            "unitPrice": {
                "value": bill_trans_item['up'],
                "currency": "THB"
            },
            "net": {
                "value": bill_trans_item['charge_amt'],
                "currency": "THB"
            },
            "extension": [
                {
                    "url": "https://sil-th.org/fhir/StructureDefinition/claim",
                    "extension": [
                        {
                            "url": "unit",
                            "valueMoney": {
                                "value": bill_trans_item['charge_up'],
                                "currency": "THB"
                            }
                        },
                        {
                            "url": "net",
                            "valueMoney": {
                                "value": bill_trans_item['claim_amt'],
                                "currency": "THB"
                            }
                        }
                    ]
                }
            ],
            "encounter": [
                {
                    "reference": f"urn:uuid:Encounter/D/{combined_data['disp_id']}",
                }
            ]
        }
        sequence += 1
    # if 
    # repeat_drug = {
    #     "url": "https://sil-th.org/fhir/StructureDefinition/multiple-dispense",
    #     "extension": [
    #         {
    #             "url": "repeat",
    #             "extension": [
    #                 {
    #                     "url": "numberOfRepeat",
    #                     "valueUnsignedInt": !?<<BILLDISP.DispensedItem.MultiDisp:numberOfRepeat>>
    #                 },
    #                 {
    #                     "url": "numberOfRepeatsAllowed",
    #                     "valueUnsignedInt": !?<<BILLDISP.DispensedItem.MultiDisp:numberOfRepeatsAllowed>>
    #                 }
    #             ]
    #         },
    #         {
    #             "url": "period",
    #             "extension": [
    #                 {
    #                     "url": "!?<<<<BILLDISP.DispensedItem.MultiDisp:type>>",
    #                     "valueTiming": {
    #                         "repeat": {
    #                             "boundsDuration": {
    #                                 "value": !?<<BILLDISP.DispensedItem.MultiDisp:duration>>,
    #                                 "unit": "!?<<BILLDISP.DispensedItem.MultiDisp:durationUnit>>"
    #                             },
    #                             "period": !?<<BILLDISP.DispensedItem.MultiDisp:interval>>,
    #                             "periodUnit": "!?<<BILLDISP.DispensedItem.MultiDisp:intervalUnit>>"
    #                         }
    #                     }
    #                 }
    #             ]
    #         }
    #     ]
    # }
    json_data = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "fullUrl": f"urn:uuid:Organization/{h_code}",
                "resource": {
                    "resourceType": "Organization",
                    "identifier": [
                        {
                            "system": "https://bps.moph.go.th/hcode/5",
                            "value": f"{h_code}"
                        }
                    ],
                    "name": f"{h_name}"
                },
                "request": {
                    "method": "PUT",
                    "url": f"Organization/{h_code}",
                    "ifNoneExist": f"identifier=https://bps.moph.go.th/hcode/5|{h_code}"
                }
            },
            {
                "fullUrl": f"urn:uuid:Patient/{h_code}/{combined_data['hn']}",
                "resource": {
                    "resourceType": "Patient",
                    "text": {
                        "status": "extensions",
                        "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">{combined_data['name']} (HN: {combined_data['hn']})</div>"
                    },
                    "identifier": patient_identifiers,
                    "name": [
                        {
                            "text": f"{combined_data['name']}"
                        }
                    ],
                    "generalPractitioner": [
                        {
                            "type": "Organization",
                            "identifier": {
                                "system": "https://bps.moph.go.th/hcode/5",
                                "value": f"{h_code}"
                            }
                        }
                    ],
                    "managingOrganization": {
                        "reference": f"urn:uuid:Organization/{h_code}"
                    }
                },
                "request": {
                    "method": "PUT",
                    "url": f"Patient?identifier=https://sil-th.org/CSOP/hn|{combined_data['hn']}",
                    "ifNoneExist": f"identifier=https://sil-th.org/CSOP/hn|{combined_data['hn']}"
                }
            },
            {
                "fullUrl": f"urn:uuid:Location/{combined_data['station']}",
                "resource": {
                    "resourceType": "Location",
                    "text": {
                        "status": "generated",
                        "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">Station ID: {combined_data['station']}</div>"
                    },
                    "identifier": [
                        {
                            "system": "https://sil-th.org/CSOP/station",
                            "value": f"{combined_data['station']}"
                        }
                    ],
                    "type": [
                        {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                                    "code": "BILL",
                                    "display": "Billing Contact"
                                }
                            ]
                        }
                    ],
                    "managingOrganization": {
                        "reference": f"urn:uuid:Organization/{h_code}"
                    }
                },
                "request": {
                    "method": "PUT",
                    "url": f"Location?identifier=https://sil-th.org/CSOP/station|{combined_data['station']}",
                    "ifNoneExist": f"identifier=https://sil-th.org/CSOP/station|{combined_data['station']}"
                }
            },
            # {
            #     "fullUrl": f"urn:uuid:Practitioner/{combined_data['practitioner']['type']}/{combined_data['license_id'][1:]}",
            #     "resource": {
            #         "resourceType": "Practitioner",
            #         "text": {
            #             "status": "extensions",
            #             "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">{combined_data['license_id']}</div>"
            #         },
            #         "identifier": [
            #             {
            #                 "type": {
            #                     "coding": [
            #                         {
            #                             "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            #                             "code": f"{combined_data['practitioner']['type']}"
            #                         }
            #                     ]
            #                 },
            #                 "system": f"{combined_data['practitioner']['system']}",
            #                 "value": f"{combined_data['license_id'][1:]}"
            #             }
            #         ]
            #     },
            #     "request": {
            #         "method": "PUT",
            #         "url": f"Practitioner?identifier={h_code}|{combined_data['license_id'][1:]}",
            #         "ifNoneExist": f"identifier={combined_data['practitioner']['system']}|{combined_data['license_id'][1:]}"
            #     }
            # },
            {
                "fullUrl": f"urn:uuid:Encounter/D/{combined_data['disp_id']}",
                "resource": {
                    "resourceType": "Encounter",
                    "text": {
                        "status": "extensions",
                        "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">Dispense ID: {combined_data['disp_id']} (HN: {combined_data['hn']})<p>service: Pharmacy | status: {disp_status_mapping[combined_data['disp_status']]}</p></div>"
                    },
                    "identifier": [
                        {
                            "system": "https://sil-th.org/CSOP/dispenseId",
                            "value": f"{combined_data['disp_id']}"
                        }
                    ],
                    "status": "finished",
                    "class": {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                        "code": "AMB"
                    },
                    "serviceType": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/service-type",
                                "code": "64",
                                "display": "Pharmacy"
                            }
                        ]
                    },
                    "subject": {
                        "reference": f"urn:uuid:Patient/{h_code}/{combined_data['hn']}"
                    },
                    "participant": [
                        {
                            "individual": {
                                "reference": f"urn:uuid:Practitioner/{combined_data['practitioner']['type']}/{combined_data['license_id'][1:]}"
                            }
                        }
                    ],
                    "period": {
                        "start": f"{combined_data['presc_date']}",
                        "end": f"{combined_data['disp_date']}"
                    },
                    "serviceProvider": {
                        "reference": f"urn:uuid:Organization/{h_code}"
                    },
                },
                "request": {
                    "method": "PUT",
                    "url": f"Encounter?identifier=https://sil-th.org/CSOP/dispenseId|{combined_data['disp_id']}",
                    "ifNoneExist": f"identifier=https://sil-th.org/CSOP/dispenseId|{combined_data['disp_id']}"
                }
            },
            {
                "fullUrl": f"urn:uuid:MedicationDispense/{combined_data['disp_id']}/{combined_data['local_drug_id']}",
                "resource": {
                    "resourceType": "MedicationDispense",
                    "text": {
                        "status": "extensions",
                        "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">Dispense ID: {combined_data['disp_id']} (HN: {combined_data['hn']})<p>{combined_data['dfs']} - {combined_data['instruction_text']}</p><p>QTY: {combined_data['quantity']} {combined_data['package_size']}</p></div>"
                    },
                    "extension": [
                        {
                            "url": "https://sil-th.org/fhir/StructureDefinition/product-category",
                            "valueCodeableConcept": {
                                "coding": [
                                    {
                                        "system": "https://sil-th.org/fhir/CodeSystem/csop-productCategory",
                                        "code": f"{combined_data['product_cat']}"
                                    }
                                ]
                            }
                        },
                        # **repeat_drug
                    ],
                    "identifier": [
                        {
                            "system": "https://sil-th.org/CSOP/dispenseId",
                            "value": f"{combined_data['disp_id']}"
                        }
                    ],
                    "status": f"{disp_status_mapping[combined_data['disp_status']]}",
                    "category": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/fhir/CodeSystem/medicationdispense-category",
                                "code": "outpatient"
                            }
                        ]
                    },
                    "medicationCodeableConcept": {
                        "coding": [
                            {
                                "system": "https://sil-th.org/CSOP/localCode",
                                "code": f"{combined_data['local_drug_id']}"
                            },
                            {
                                "system": "https://tmt.this.or.th",
                                "code": f"{combined_data['standard_drug_id']}"
                            }
                        ],
                        "text": f"{combined_data['dfs']}"
                    },
                    "subject": {
                        "reference": f"urn:uuid:Patient/{h_code}/{combined_data['hn']}",
                    },
                    "context": {
                        "reference": f"urn:uuid:Encounter/D/{combined_data['disp_id']}"
                    },
                   "performer": [
                        {
                            "actor": {
                                "reference": f"urn:uuid:Organization/{h_code}"
                            }
                        }
                    ],
                    "quantity": {
                        "value": combined_data['quantity'],
                        "unit": f"{combined_data['package_size']}"
                    },
                    # "daysSupply": {
                    #     "value": !?<<BILLDISP.DispensedItem.SupplyFor:Number>>,
                    #     "unit": "!?<<BILLDISP.DispensedItem.SupplyFor:Unit>"
                    # },
                    "whenHandedOver": f"{combined_data['disp_date']}",
                    "dosageInstruction": [
                        {
                            "text": f"{combined_data['instruction_text']}",
                            "timing": {
                                "code": {
                                    "text": f"{combined_data['instruction_code']}"
                                }
                            }
                        }
                    ],
                    # "substitution": {
                    #     "wasSubstituted": prd_code_flag[combined_data['prd_code']],
                    #     "type": {
                    #         "coding": [
                    #             {
                    #                 "system": "https://sil-th.org/fhir/CodeSystem/csop-substitutionAllowed",
                    #                 "code": f"{combined_data['prd_code']}"
                    #             }
                    #         ]
                    #     }
                    # }
                },
                "request": {
                    "method": "PUT",
                    "url": f"MedicationDispense?identifier=https://sil-th.org/CSOP/dispenseId|{combined_data['disp_id']}&code=https://sil-th.org/CSOP/localCode|{combined_data['local_drug_id']}",
                    "ifNoneExist": f"identifier=https://sil-th.org/CSOP/dispenseId|{combined_data['disp_id']}&code=https://sil-th.org/CSOP/localCode|{combined_data['local_drug_id']}",
                }
            }
        ]
    }
    # print(json.dumps(json_data))
    # break
    res = requests.post(base_fhir_url, json=json_data)
    print(res.status_code)
    print(res.content)

