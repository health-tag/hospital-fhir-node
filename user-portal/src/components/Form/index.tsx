import React, {
  Dispatch,
  FormEvent,
  SetStateAction,
  useEffect,
  useState,
} from "react";

type Validation = {
  [fieldName: string]: { valid: boolean; messages: string[] };
};

export const FormContext = React.createContext<{
  validations: Validation;
  setValidation: (validation: Validation) => void;
}>({
  validations: {},
  setValidation: (validation: Validation) => {},
});

export class ValidationBuilder {
  private obj: Validation = {};

  public addValidation(key: string, valid: boolean, message?: string) {
    if (this.obj[key] === undefined) {
      if (message) {
        this.obj[key] = { valid: valid, messages: [message] };
      } else {
        this.obj[key] = { valid: valid, messages: [] };
      }
    } else {
      if (message) {
        this.obj[key].valid = valid;
        this.obj[key].messages.push(message);
      } else {
        this.obj[key].valid = valid;
      }
    }
    return this;
  }

  public build() {
    return this.obj;
  }
}

export const Form = ({
  children,
  onValidSubmit,
  onValidityChange,
  ...otherProps
}: {
  children: React.ReactNode;
  onValidSubmit: Function;
  onValidityChange?:
    | ((valid: boolean) => {})
    | Dispatch<SetStateAction<boolean>>;
  [x: string]: any;
}) => {
  const [isValid, setIsValid] = useState(false);
  const [validations, setValidations] = useState<Validation>({});

  const setValidation = (validation: Validation) => {
    const obj = { ...validations, ...validation };
    setValidations(obj);
  };

  useEffect(() => {
    let _isValid = true;
    for (const fieldValidation in formContext.validations) {
      if (formContext.validations.hasOwnProperty(fieldValidation)) {
        _isValid = _isValid && formContext.validations[fieldValidation].valid;
      }
    }
    if (_isValid !== isValid) {
      setIsValid(_isValid);
      onValidityChange && onValidityChange(_isValid);
    }
  }, [validations]);

  const handleOnSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (isValid) {
      onValidSubmit();
    }
  };

  const formContext = {
    validations: validations,
    setValidation: setValidation,
    //clearValidation: clearValidation,
  };

  return (
    <FormContext.Provider value={formContext}>
      <form {...otherProps} onSubmit={handleOnSubmit}>
        {children}
      </form>
    </FormContext.Provider>
  );
};
