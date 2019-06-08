export  class LookupHelper {
  public static createLookup<T>(getKey: (item: T) => string, items: T[]) {
    const lookup = new Map<string, T[]>()
    items.forEach(item => {
      let key = getKey(item)
      if (!lookup[key]) {
        lookup[key] = [item]
      } else {
        lookup[key].push(item)
      }
    })

    return lookup
  }

}
