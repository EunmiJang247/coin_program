import useLogic from './use-logic';
import Loading from '../../components/loading';
import Failed from '../../components/failed';
import MenuBarApp from '../../components/menu-bar-app';
import TestBannerApp from '../../components/test-banner-app';
import FooterApp from '../../components/footer-app';
import TestExplorerFragment from './fragments/test-explorer';
import styles from './index.module.scss';

const MainPage = () => {
  const logic = useLogic();

  if (logic.status === 'LOADING') {
    return <Loading />;
  }

  if (logic.status === 'FAILED') {
    return <Failed logic={logic} />;
  }

  return (
    <>
      <MenuBarApp />
      <TestBannerApp />
      <TestExplorerFragment logic={logic} />
      <FooterApp className={styles.footer} />
    </>
  );
};

export default MainPage;
