import { FormContext, ValidationBuilder } from "@components/Form";
import { nameof } from "@utilities/ts";
import { ChangeEvent, useContext, useEffect, useState } from "react";

const Input = ({
  id = Math.random()
    .toString(36)
    .replace(/[^a-z]+/g, "")
    .substring(0, 6),
  label = "",
  name = "",
  type,
  placeholder,
  required = false,
  value,
  className = "",
  inputClassName = "",
  setValue,
  validator,
  forceRevalidate,
  ...otherProps
}: {
  id?: string;
  name: string;
  label?: string;
  type?: string;
  required?: boolean;
  placeholder?: string;
  value: string;
  className?: string;
  inputClassName?: string;
  setValue: Function;
  validator?: (value: string) => {
    result: boolean;
    message?: string;
  };
  forceRevalidate?:number;
  [x: string]: any;
}) => {
  const formContext = useContext(FormContext);
  const [firstTimeRender, setFirstTimeRender] = useState<boolean>(true);

  const onChangeHandler = (event: ChangeEvent<HTMLInputElement>) => {
    setFirstTimeRender(false);
    setValue(event.target.value);
    validatorHandler(event.target.value);
  };

  const validatorHandler = (value: string) => {
    const builder = new ValidationBuilder();
    if (required && value === "") {
      builder.addValidation(name, false, "จำเป็นต้องใส่");
    } else if (validator !== undefined) {
      const { result, message } = validator(value);
      builder.addValidation(name, result);
      if (!result) {
        builder.addValidation(name, result, message!);
      }
    } else {
      builder.addValidation(name, true);
    }
    formContext.setValidation(builder.build());
  };

  useEffect(() => {
    validatorHandler(value);
  }, []);

  useEffect(() => {
    validatorHandler(value);
  }, [forceRevalidate]);

  return (
    <div className={className}>
      <label htmlFor={id} className="block pb-1">
        {label}
      </label>
      <input
        id={id}
        name={name}
        className={` ${inputClassName} ${
          !formContext.validations[name]?.valid && !firstTimeRender
            ? "required"
            : ""
        } `}
        type={type ? type : "text"}
        placeholder={placeholder}
        value={value}
        onChange={onChangeHandler}
        {...otherProps}
      />
      <div className="text-sm pt-1">
        {!formContext.validations[name]?.valid && !firstTimeRender && (
          <span className="text-red-400">
            {formContext.validations[name]?.messages.join(" ")}
          </span>
        )}
      </div>
    </div>
  );
};
export default Input;
