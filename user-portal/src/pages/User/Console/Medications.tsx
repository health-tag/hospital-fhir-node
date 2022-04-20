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
  const navigate = useNavigate();

  const [prescriptions, setPrescriptionList] = useState<Array<Prescription>>(
    []
  );
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [name, setName] = useState<string | null>("");
  const [hn, setHN] = useState<string | null>("");

  useEffect(() => {
    const username = sessionStorage.getItem("username")!;
    const password = sessionStorage.getItem("password")!;
    const hn = sessionStorage.getItem("hn");
    if (!hn) {
      navigate("/", { replace: true });
    }
    setHN(hn);
    axios
      .get(
        `${process.env.REACT_APP_KONG_URL}/fhir-api/Patient?identifier=https%3A%2F%2Fsil-th.org%2FCSOP%2Fhn%7C${hn}`,
        {
          auth: {
            username: username,
            password: password,
          },
        }
      )
      .then((patientResponse) => {
        const patientInfo = patientResponse.data.entry[0].resource;
        const patientID = patientInfo.id;
        // Temporary workaround for the name data which is still included "ชื่อ"
        const nameRegexResult = nameRegex.exec(patientInfo.name[0].text.trim());
        const name = nameRegexResult?.groups?.name ?? "";
        const surname = nameRegexResult?.groups?.surname ?? "";
        setName(`${name} ${surname}`);
        let prescriptions: Array<Prescription> = [];
        axios
          .get(
            `${process.env.REACT_APP_KONG_URL}/fhir-api/Patient/${patientID}/$everything?_format=json`,
            {
              auth: {
                username: username,
                password: password,
              },
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
      <h3 className="page-h">
        <MedicationIcon className="h-8 w-8 inline-block mr-3" />
        รายการยา
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
