const { InfluxDB, Point } = require('@influxdata/influxdb-client');

let writeApi;
let queryApi;

const initInfluxDB = () => {
  try {
    const client = new InfluxDB({
      url: process.env.INFLUXDB_URL,
      token: process.env.INFLUXDB_TOKEN,
    });

    writeApi = client.getWriteApi(
      process.env.INFLUXDB_ORG,
      process.env.INFLUXDB_BUCKET,
      'ns'
    );

    queryApi = client.getQueryApi(process.env.INFLUXDB_ORG);

    console.log('✅ InfluxDB conectado');
    return { writeApi, queryApi };
  } catch (error) {
    console.error('❌ Error conectando a InfluxDB:', error.message);
    process.exit(1);
  }
};

const getWriteApi = () => writeApi;
const getQueryApi = () => queryApi;

module.exports = {
  initInfluxDB,
  getWriteApi,
  getQueryApi,
  Point,
};
