import axios from 'axios';

export const URL = 'http://127.0.0.1:5000';

// const channelId = 'UCZCFT11CWBi3MHNlGf019nw';

export async function getStats(route) {
  if (route === '/channel-details/') return;
  const res = await axios.get(`${URL}/${route}`);
  return res.data;
}

export async function getSentiments(route) {
  const res = await axios.get(`${URL}/${route}`);
  return res.data;
}
