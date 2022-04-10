import Bg from "@assets/images/login-bg.svg";

const BlankLayout = ({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <div className={`min-w-screen min-h-screen bg-primary-gradient-light-5.5`}>
      <img className="absolute w-full h-full object-cover" src={Bg} />
      <div className={`${className} relative z-10`}>{children}</div>
    </div>
  );
};
export default BlankLayout;
