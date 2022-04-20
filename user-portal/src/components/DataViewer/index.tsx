import { Placeholder } from "@components/Placeholder";

export const DataViewer = ({
  isLoading = false,
  label,
  deferredChildren,
  ...otherProps
}: {
  isLoading: boolean | any;
  label?: string;
  deferredChildren: (() => React.ReactNode) | (() => string) | (() => number);
  [x: string]: any;
}) => (
  <div {...otherProps}>
    {label && <div className="text-sm">{label}</div>}
    {isLoading ? <div>{deferredChildren()}</div> : <Placeholder />}
  </div>
);
