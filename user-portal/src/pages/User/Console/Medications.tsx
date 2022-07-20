import { useState, useEffect, Fragment } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import { pageAnimationVariants } from "@animations/variants";
import { motion } from "framer-motion";
import { MedicationIcon } from "@components/Icons";
import { TrPlaceholder } from "@components/Placeholder";

type Quantity = {
  value: number;
  unit: string;
};

type Prescription = {
  displayText: string;
  dosageInstruction: string;
  whenHandedOver: string;
  quantity: Quantity;
};

const nameRegex = /(ชื่อ|)\s+(?<name>\S+)\s+(?<surname>.+)/;

const MedicationsPage = () => {
  const [fhirURL, setFhirURL] = useState<string>("http://54.151.227.175:8000/fhir-api/Patient/2");
  const [prescriptions, setPrescriptionList] = useState<Array<Prescription>>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [name, setName] = useState<string | null>("");
  const [mappingType, setMappingType] = useState<string>("dispense");
  const [authHeader, setAuthHeaders] = useState<string>("")

  useEffect(() => {
    axios
      .get(
        `${fhirURL}`, {
          headers: {
            Authorization: authHeader
          }
        }
      )
      .then((patientResponse) => {
        const patientInfo = patientResponse.data;
        const patientID = patientInfo.id;
        // Temporary workaround for the name data which is still included "ชื่อ"
        const nameRegexResult = nameRegex.exec(patientInfo.name[0].text.trim());
        const name = nameRegexResult?.groups?.name ?? "";
        const surname = nameRegexResult?.groups?.surname ?? "";
        setName(`${name} ${surname}`);
        let prescriptions: Array<Prescription> = [];
        axios
          .get(
            `${fhirURL}/$everything?_format=json`, {
                headers: {
                Authorization: authHeader
              }
            }
          )
          .then((response) => {
            for (const resource of response.data.entry) {
              if (resource.resource.resourceType == "MedicationDispense" && mappingType == "dispense") {
                const data = {
                  displayText: resource.resource.medicationCodeableConcept.text,
                  dosageInstruction:
                    resource.resource.dosageInstruction[0].text,
                  whenHandedOver:
                    resource.resource.whenHandedOver.split("T")[0],
                  quantity: resource.resource.quantity,
                };
                prescriptions.push(data);
              }
              if (resource.resource.resourceType == "MedicationRequest" && mappingType == "request") {
                const data = {
                  displayText: resource.resource.medicationCodeableConcept.text,
                  dosageInstruction: "",
                  whenHandedOver:
                    resource.resource.authoredOn.split("T")[0],
                  quantity: resource.resource.quantity,
                };
                prescriptions.push(data);
              }
            }
            setPrescriptionList(prescriptions);
          });
      })
      .catch((error) => {
        setPrescriptionList([]);
        setName("");
      })
  }, [fhirURL, mappingType, authHeader]);

  useEffect(() => {
    axios
      .get(
        `${fhirURL}`, {
          headers: {
            Authorization: authHeader
          }
        }
      )
      .then((patientResponse) => {
        const patientInfo = patientResponse.data;
        const patientID = patientInfo.id;
        // Temporary workaround for the name data which is still included "ชื่อ"
        const nameRegexResult = nameRegex.exec(patientInfo.name[0].text.trim());
        const name = nameRegexResult?.groups?.name ?? "";
        const surname = nameRegexResult?.groups?.surname ?? "";
        setName(`${name} ${surname}`);
        let prescriptions: Array<Prescription> = [];
        axios
          .get(
            `${fhirURL}/$everything?_format=json`, {
              headers: {
                Authorization: authHeader
              }
            }
          )
          .then((response) => {
            for (const resource of response.data.entry) {
              if (resource.resource.resourceType == "MedicationDispense") {
                const data = {
                  displayText: resource.resource.medicationCodeableConcept.text,
                  dosageInstruction:
                    resource.resource.dosageInstruction[0].text,
                  whenHandedOver:
                    resource.resource.whenHandedOver.split("T")[0],
                  quantity: resource.resource.quantity,
                };
                prescriptions.push(data);
              }
            }
            setPrescriptionList(prescriptions);
          });
      });
  }, []);

  return (
    <motion.div
    variants={pageAnimationVariants}
    initial="initial"
    animate="animate"
    exit="exit"
  >
    <div className="shadow overflow-hidden sm:rounded-md">
      <div className="px-4 py-5 bg-white sm:p-6">
        <div className="grid grid-cols-6 gap-6">
          <div className="col-span-6 sm:col-span-3">
            <label htmlFor="fhir-base" className="block text-sm font-medium text-gray-700">
              FHIR base URL
            </label>
            <input
              placeholder="https://..../fhir"
              onChange={(e) => setFhirURL(e.target.value)}
              type="text"
              name="fhir-base"
              id="fhir-base"
              className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            />
          </div>
          <div className="col-span-6 sm:col-span-3">
            <label htmlFor="auth" className="block text-sm font-medium text-gray-700">
              Headers Authentication value (optional)
            </label>
            <input
              placeholder="Bearer ..."
              onChange={(e) => setAuthHeaders(e.target.value)}
              type="text"
              name="auth"
              id="auth"
              className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
            />
          </div>
          <div className="col-span-6 sm:col-span-3">
            <label htmlFor="mapping-type" className="block text-sm font-medium text-gray-700">
              Mapping Type
            </label>
            <select
              id="mapping-type"
              name="mapping-type"
              className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              onChange={(e) => setMappingType(e.target.value)}
            >
              <option value="dispense">MedicationDispense</option>
              <option value="request">MedicationRequest</option>
            </select>
          </div>
        </div>
      </div>
    </div>
      <h3 className="page-h">
        <MedicationIcon className="h-8 w-8 inline-block mr-3" />
        รายการยา ของ {name}
      </h3>
      {isLoading ? (
        <section className="card">
          <table className="table-style-1">
            <thead>
              <tr>
                <th className="col text-sm font-mediumpx-6 py-4 px-4">
                  ชื่อยา
                </th>
                <th className="col text-sm font-mediumpx-6 py-4 px-4">
                  วิธีใช้
                </th>
                <th className="col text-sm font-mediumpx-6 py-4 px-4">
                  ปริมาณ
                </th>
              </tr>
            </thead>
            <tbody>
              <TrPlaceholder rows={6} columns={3} />
            </tbody>
          </table>
        </section>
      ) : (
        <>
          {prescriptions
            .groupBySameDay("whenHandedOver")
            .map(({ key, value }, index) => (
              <Fragment key={index}>
                <h4 className="page-h">
                  {key.toLocaleDateString("th-TH", {
                    weekday: "long",
                    day: "numeric",
                    month: "long",
                    year: "numeric",
                  })}
                </h4>
                {value.groupBy("hosName").map(({ key, value }, index) => (
                  <Fragment key={index}>
                    <h5 className="page-h">{key}</h5>
                    <section className="card mb-6">
                      <table className="table-style-1">
                        <thead>
                          <tr>
                            <th>ชื่อยา</th>
                            <th>วิธีใช้</th>
                            <th>ปริมาณ</th>
                          </tr>
                        </thead>
                        <tbody>
                          {value.map((item, index) => {
                            return (
                              <tr key={index}>
                                <td>{item.displayText}</td>
                                <td>{item.dosageInstruction}</td>
                                <td>
                                  {item.quantity.value} ({item.quantity.unit})
                                </td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </section>
                  </Fragment>
                ))}
              </Fragment>
            ))}
        </>
      )}
    </motion.div>
  );
};
export default MedicationsPage;
