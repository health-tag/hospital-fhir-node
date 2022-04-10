export {};
declare global {
  export interface Array<T> {
    groupBy(
      this: T[],
      propertyName: string | number
    ): { key: string; value: T[] }[];
    groupBySameDay(
      this: T[],
      propertyName: string | number
    ): { key: Date; value: T[] }[];
  }
}
Array.prototype.groupBy = function <T>(
  this: T[],
  propertyName: string | number
): { key: string; value: T[] }[] {
  const result = this.reduce((acc, obj) => {
    const key = obj[propertyName];
    const target = acc.find((a) => a.key === key);
    if (target === undefined) {
      acc.push({ key: key, value: [obj] });
    } else {
      target.value.push(obj);
    }
    return acc;
  }, new Array<{ key: string; value: T[] }>());
  return result;
};

Array.prototype.groupBySameDay = function <T>(
  this: T[],
  datePropertyName: string | number
): { key: Date; value: T[] }[] {
  const result = this.reduce((acc, obj) => {
    const key = new Date(obj[datePropertyName]);
    const dateKey = new Date(key.getFullYear(), key.getMonth(), key.getDate());
    const target = acc.find((a) => a.key.getTime() === dateKey.getTime());
    if (target === undefined) {
      acc.push({ key: dateKey, value: [obj] });
    } else {
      target.value.push(obj);
    }
    return acc;
  }, new Array<{ key: Date; value: T[] }>());
  return result;
};
