import { useState, useEffect, Fragment } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { pageAnimationVariants } from "@animations/variants";
import { motion } from "framer-motion";
import { FoodAllergyIcon } from "@components/Icons";
import { TrPlaceholder } from "@components/Placeholder";

type AllergyIntolerance = {
  recordedDate: Date;
  displayName: string;
  criticality: string;
  verificationStatus: string;
  symptom: string;
};

const AllergiesPage = () => {
  const navigate = useNavigate();

  const [allergies, setAllergies] = useState<
    Array<AllergyIntolerance>
  >([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [name, setName] = useState<string | null>("");
  const [hn, setHN] = useState<string | null>("");

  useEffect(() => {
    const loadData = async () => {
      const allergies = new Array<AllergyIntolerance>();
      setIsLoading(true);
      const username = sessionStorage.getItem("username")!;
      const password = sessionStorage.getItem("password")!;
      const hn = sessionStorage.getItem("hn");
      if (!hn) {
        navigate("/", { replace: true });
      }
      setHN(hn);
      let response = await axios.get(
        `${process.env.REACT_APP_KONG_URL}/fhir-api/AllergyIntolerance?patient.identifier=https://sil-th.org/CSOP/hn%7C${hn}`,
        {
          auth: {
            username: username,
            password: password,
          },
        }
      );
      for (const { resource } of response.data.entry) {
        if (resource.resourceType == "AllergyIntolerance") {
          const data = {
            recordedDate: resource.recordedDate,
            displayName: resource.code.coding[0].display,
            criticality: resource.criticality,
            verificationStatus: resource.verificationStatus.coding[0].code,
            symptom: resource.reaction.map(
              ({ manifestation }) => manifestation[0].coding[0].display
            ),
          };
          allergies.push(data);
        }
      }
      setAllergies(allergies);
      setIsLoading(false);
    };

    loadData();
  }, []);

  return (
    <motion.div
      variants={pageAnimationVariants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      <h3 className="page-h">
        <FoodAllergyIcon className="h-8 w-8 inline-block mr-3" />
        แพ้ยา
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
        <section className="card mb-6">
          <table className="table-style-1">
            <thead>
              <tr>
                <th>วันที่บันทึก</th>
                <th>ชื่อยา</th>
                <th>การตรวจสอบ</th>
                <th>ความรุนแรง</th>
                <th>อาการ</th>
              </tr>
            </thead>
            <tbody>
              {allergies.map((allergen, index) => (
                <Fragment key={index}>
                  <tr key={index}>
                    <td>{`${allergen.recordedDate}`}</td>
                    <td>{allergen.displayName}</td>
                    <td>{allergen.verificationStatus}</td>
                    <td>{allergen.criticality}</td>
                    <td>{allergen.symptom}</td>
                  </tr>
                </Fragment>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </motion.div>
  );
};
export default AllergiesPage;
