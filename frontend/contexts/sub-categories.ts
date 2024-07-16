import { createContext } from 'react';
import SubCategory from '../data-types/sub-category';

// TODO 에러를 감지할 수 없는 undefined를 여기에서 쓰는게 맞을까?
const SubCategoriesContext = createContext<SubCategory[] | undefined>(undefined);

export default SubCategoriesContext;
