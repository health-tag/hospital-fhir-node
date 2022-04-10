export const Placeholder = () => (
  <div className="placeholder">
    <div className="placeholder-activity"></div>
  </div>
);

export const TrPlaceholder = ({rows = 1, columns = 1}) => {
  const key = Math.trunc((Math.random()*1000))
  const columnElements = [...Array(columns)].map((c,index)=><td key={`${index}`}><Placeholder/></td>)
  const rowElements = [...Array(rows)].map((r,index)=><tr key={`${index}`}>{columnElements}</tr>)
  return <>{rowElements}</>
};
