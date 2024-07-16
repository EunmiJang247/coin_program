import '../styles/globals.css';
import type { AppProps } from 'next/app';
import SubCategoriesProvider from '../providers/sub-categories';

const App: React.FC<AppProps> = ({ Component, pageProps }) => {
  return (
    <SubCategoriesProvider>
      {/* eslint-disable-next-line react/jsx-props-no-spreading */}
      <Component {...pageProps} />
    </SubCategoriesProvider>
  );
};

export default App;
