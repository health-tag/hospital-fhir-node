import { FormContext } from "@components/Form";
import { LoadingIcon } from "@components/Icons";
import { useContext } from "react";

type Props = {
  mode?: "primary" | "secondary" | "danger";
  type?: "submit" | "reset" | "button";
  isLoading?: boolean;
  className?: string;
  disabled?: boolean;
  onClick?: Function;
  children?: React.ReactNode;
};

const Button = (props: Props) => {
  const {
    mode = "",
    type = "button",
    children,
    isLoading,
    className = "",
    disabled = false,
    onClick,
  } = props;

  const handlerOnClick = () => {
    if (onClick === undefined || onClick == null) return;
    onClick();
  };

  return (
    <button
      className={`w-full ${mode} ${className} ${isLoading ? "working" : ""}`}
      type={type}
      disabled={disabled}
      onClick={handlerOnClick}
    >
      {isLoading ? (
        <div className="flex items-center gap-2 justify-center">
          <LoadingIcon spinning={true} />
          <span>กำลังดำเนินการ</span>
        </div>
      ) : (
        <div className="flex items-center gap-2 justify-center">{children}</div>
      )}
    </button>
  );
};
export default Button;
