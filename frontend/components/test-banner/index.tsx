import styles from './index.module.scss';

const TestBanner: React.FC = () => {
  return (
    <div className={styles.cont}>
      <span className="text-3xl p3 text-lime-400">TestBanner</span>
    </div>
  );
};

export default TestBanner;
