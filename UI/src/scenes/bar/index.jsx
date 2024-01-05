import { Box } from "@mui/material";
import BarChart from "../../components/barchart";
import Header from "../../components/header";

const Bar = () => {
  return (
    <Box m="20px">
      <Header title="BarChart" subtitle="Simple Bar Chart" />
      <Box height="75vh">
        <BarChart />
      </Box>
    </Box>
  );
};

export default Bar;
