import Footer from '../footer';

interface FooterAppProps {
  className?: string | undefined;
}

const FooterApp: React.FC<FooterAppProps> = ({ className }) => <Footer className={className} />;

export default FooterApp;
