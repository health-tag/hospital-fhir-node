import Button from "@components/Button";
import { AcceptIcon } from "@components/Icons";

export const Modal = ({ children, title = "", buttons }) => {
    return (
      <div className="bg-glass fixed w-screen min-h-screen flex items-center justify-center top-0 left-0">
        <div className="modal rounded-xl shadow-lg m-6">
          <div className="text-white py-3 px-6">{title}</div>
          <div className="content-area p-6 bg-white">{children}</div>
          <div className="button-area p-6 bg-gray-200 flex gap-6">{buttons}</div>
        </div>
      </div>
    );
  };
  
export const AlertModal = ({ title = "", children, onAccept = () => {} }) => {
    return (
      <Modal
        title={title}
        buttons={
          <Button mode="primary" onClick={onAccept}>
            <AcceptIcon /> ตกลง
          </Button>
        }
      >
        {children}
      </Modal>
    );
  };