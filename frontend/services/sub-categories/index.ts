import { useContext } from 'react';
import SubCategoriesContext from '../../contexts/sub-categories';

const useSubCategories = () => {
  const categories = useContext(SubCategoriesContext);

  return categories;
};

export default useSubCategories;
