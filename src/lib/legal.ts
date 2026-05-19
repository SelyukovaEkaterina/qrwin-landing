/** Реквизиты оператора персональных данных (сайт qrstars.ru) */
export const OPERATOR = {
  name: 'ИП Красников Иван Геннадьевич',
  fullName: 'Индивидуальный предприниматель Красников Иван Геннадьевич',
  inn: '540536312882',
  site: 'https://qrstars.ru',
  email: 'support@qrstars.ru',
} as const;

export const LEGAL_LINKS = {
  privacy: '/politika-konfidencialnosti.html',
  consent: '/soglasie-pd.html',
} as const;

/** API предрегистрации (приложение QrStars) */
export const PREREG_API_URL = 'https://app.qrstars.ru/api/waitlist';
