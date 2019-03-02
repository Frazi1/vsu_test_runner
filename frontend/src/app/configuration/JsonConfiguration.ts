import { JsonConvert, ValueCheckingMode } from 'json2typescript';

class JsonConfiguration {
  public static createJson(): JsonConvert {
    const json = new JsonConvert();
    json.valueCheckingMode = ValueCheckingMode.ALLOW_NULL;
    return json;
  }
}

export const jsonConvert: JsonConvert = JsonConfiguration.createJson();
