import { useEffect, useState } from 'react';
import SubCategoriesContext from '../contexts/sub-categories';
import SubCategory from '../data-types/sub-category';
import useReadSubCategories from '../services/read-sub-categories';

interface Props {
  children?: any;
}

const SubCategoriesProvider: React.FC<Props> = ({ children }) => {
  const readSubCategories = useReadSubCategories();
  const [categories, setCategories] = useState<SubCategory[] | undefined>(undefined);

  const init = async () => {
    // eslint-disable-next-line no-underscore-dangle
    const categories_ = await readSubCategories();
    setCategories(categories_);
  };

  useEffect(() => {
    init();
  }, []);

  return <SubCategoriesContext.Provider value={categories}>{children}</SubCategoriesContext.Provider>;
};

export default SubCategoriesProvider;
