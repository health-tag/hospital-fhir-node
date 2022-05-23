from ast import literal_eval
import requests

#region Configuration

headers = {
    'apikey': ''
}

#endregion 

def print_response(res_json_byte):
    result = literal_eval(res_json_byte.decode('utf8'))  # json.load(res_json)
    try:
        for e in result["entry"]:
            e = e["response"]
            if("outcome" in e):
                print(e["status"], e["location"], e["outcome"])
            else:
                print(e["status"], e["location"])
    except:
        print(result)

def create_fhir_transaction(entries):
    return {"resourceType": "Bundle",
            "type": "batch", "entry": entries}

def batch_post_bundule(entries,base_fhir_url,batch_size):
    print(f"POST: {entries[0]['resource']['resourceType']} (", len(entries), "items )")
    i = 0

    while i < len(entries):
        j = i+batch_size
        if j+1 >= len(entries):
            j = len(entries)-1
        print(i, "-", j)
        if i==j:
            res = requests.post(base_fhir_url, json=create_fhir_transaction(
            entries[i]), headers=headers)
        else:
            res = requests.post(base_fhir_url, json=create_fhir_transaction(
            entries[i:j]), headers=headers)
        print_response(res.content)
        i = i+batch_size