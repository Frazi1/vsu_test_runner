export class TimeUtils {
  public static getFormatterDurationString(timeInSeconds: number) {
    const minutes = Math.trunc(timeInSeconds / 60)
    if (minutes < 1) {
      return `${timeInSeconds} сек.`
    }
    const secondsLeft = timeInSeconds % 60

    const hours = Math.trunc(minutes / 60)
    if (hours < 1) {
      return `${minutes} мин. ${secondsLeft} сек`
    }
    const minutesLeft = minutes % 60

    return `${hours} час. ${minutesLeft} мин. ${secondsLeft} сек.`
  }
}
