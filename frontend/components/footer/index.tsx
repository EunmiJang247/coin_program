import styles from './index.module.scss';
import combineClassNames from '../../utils/combine-class-names';

interface Props {
  className?: string | undefined;
}

const Footer: React.FC<Props> = ({ className }) => {
  return (
    <div className={combineClassNames(styles.cont, className)}>
      <span>푸우터</span>
    </div>
  );
};

export default Footer;
