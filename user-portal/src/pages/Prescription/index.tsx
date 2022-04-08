import { Buffer } from 'buffer';
import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from 'axios';

import Logo from './../../assets/logo-header.png';

type Quantity = {
  value: number,
  unit: string
}

type Prescription = {
  displayText: string;
  dosageInstruction: string;
  whenHandedOver: string;
  quantity: Quantity;
}


const PrescriptionPage = () => {
  const navigate = useNavigate();

  const [prescriptionList, setPrescriptionList] = useState<Array<Prescription>>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [name, setName] = useState<string|null>('');
  const [hn, setHN] = useState<string|null>('');

  useEffect(() => {
    const username = sessionStorage.getItem('username')!
    const password = sessionStorage.getItem('password')!
    const hn = sessionStorage.getItem('hn')
    if (!hn) {
      navigate('/', { replace: true });
    }
    setHN(hn)
    axios.get(`${process.env.REACT_APP_KONG_URL}:8000/fhir-api/Patient?identifier=https%3A%2F%2Fsil-th.org%2FCSOP%2Fhn%7C${hn}`, {
      auth: {
        username: username,
        password: password
      }})
    .then((patientResponse) => {
      const patientInfo = patientResponse.data.entry[0].resource
      const patientID = patientInfo.id
      setName(patientInfo.name[0].text)
      let prescriptions:Array<Prescription> = [];
      axios.get(`${process.env.REACT_APP_KONG_URL}:8000/fhir-api/Patient/${patientID}/$everything?_format=json`, {
        auth: {
          username: username,
          password: password
        }})
      .then((response) => {
        for (const resource of response.data.entry) {
          if (resource.resource.resourceType == 'MedicationDispense') {
            const data = {
              displayText: resource.resource.medicationCodeableConcept.text,
              dosageInstruction: resource.resource.dosageInstruction[0].text,
              whenHandedOver: resource.resource.whenHandedOver.split('T')[0],
              quantity: resource.resource.quantity,
            };
            prescriptions.push(data);
          }
        }
        console.log(prescriptions)
        setPrescriptionList(prescriptions)
      })
    })
  }, [])

  return (

    <div className="w-full h-screen bg-blue-200">
      <div className="flex flex-auto">
        <img width="200" src={Logo} alt="" />
        <h3 className="text-gray-700 text-2xl mb-4 ml-4 p-2">{name} (HN: {hn})</h3>
      </div>
      <table className="min-w-full table-auto w-full md:w-auto">
        <thead className="bg-slate-800 border-b text-white text-left">
          <tr>
            <th className="col text-sm font-mediumpx-6 py-4 px-4">
              ชื่อยา
            </th>
            <th className="col text-sm font-mediumpx-6 py-4">
              วันที่ได้รับ
            </th>
            <th className="col text-sm font-mediumpx-6 py-4 px-4">
              ปริมาณ
            </th>
          </tr>
        </thead>
        <tbody>
          { prescriptionList.map((item, index) => {
            return (
              <tr className={`border-b text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap ${index%2==0? 'bg-white':'bg-gray-200'}`}>
                <td className="py-4 px-4">
                  <p>{item.displayText}</p>
                  <p>{item.dosageInstruction}</p>
                </td>
                <td className="py-4 px-4">
                  <p>{item.whenHandedOver}</p>
                </td>
                <td className="py-4 px-4">
                  <p>{item.quantity.value} ({item.quantity.unit})</p>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  );
}
export default PrescriptionPage;
